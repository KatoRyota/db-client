# coding: utf-8
import locale
import logging.config
import os
import platform
import re
import signal
import sys
import traceback
from ConfigParser import SafeConfigParser
from logging import Logger
from optparse import OptionParser, OptParseError
from subprocess import Popen

from context.context import Context
from runner.mysql_runner import MysqlRunner
from runner.oracle_runner import OracleRunner


class DbClient(object):
    __slots__ = (
        "__logger",
        "__context"
    )

    def __init__(self):
        # type: () -> None

        super(DbClient, self).__init__()
        reload(sys)
        sys.setdefaultencoding("utf-8")

        self.__context = Context()  # type: Context
        self.__context.root_dir = os.path.dirname(os.path.abspath(__file__))

        self.__context.profile = os.environ.get("DBCLIENT_PROFILE")

        if not self.__context.profile:
            self.__context.profile = "local"

        self.__context.config_dir = self.__context.root_dir + "/config/" + self.__context.profile

        if not os.path.isdir(self.__context.config_dir):
            raise StandardError(u"環境変数[DBCLIENT_PROFILE]が不正です。DBCLIENT_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" %
                                (self.__context.root_dir + "/config/"))

        if not os.path.isdir("./log"):
            os.makedirs("./log")

        logging.config.fileConfig(self.__context.config_dir + "/logging.conf")
        self.__logger = logging.getLogger(__name__)  # type: Logger

    @staticmethod
    def main():
        DbClient().execute()

    def execute(self):
        option_parser = OptionParser()

        # noinspection PyBroadException
        try:
            self.__logger.info("[Start] " + os.path.abspath(__file__))

            config = SafeConfigParser()
            config.read(self.__context.config_dir + "/application.conf")

            # ---- 環境変数[PYTHONIOENCODING]のチェック ----
            if os.getenv("PYTHONIOENCODING"):
                if not re.match(r"^utf[\-_]?8$", os.getenv("PYTHONIOENCODING"), re.IGNORECASE):
                    raise StandardError(u"環境変数[PYTHONIOENCODING]が不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")
            else:
                raise StandardError(u"環境変数[PYTHONIOENCODING]がセットされていません。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")

            # ---- システム環境情報を出力 ----
            self.__logger.debug("system/OS name -> " + platform.system())
            self.__logger.debug("[encoding] locale -> " + locale.getpreferredencoding())
            self.__logger.debug("[encoding] default -> " + sys.getdefaultencoding())
            self.__logger.debug("[encoding] filesystem -> " + sys.getfilesystemencoding())
            self.__logger.debug("[encoding] stdin -> " + sys.stdin.encoding)
            self.__logger.debug("[encoding] stdout -> " + sys.stdout.encoding)
            self.__logger.debug("[encoding] stderr -> " + sys.stderr.encoding)

            # ---- 起動オプションのパース ----
            option_parser.set_usage("python -m dbclient [-h][-t ARG][-f ARG][-d ARG][-l ARG][-e ARG][-b ARG][-p ARG]")

            option_parser.add_option("-t", "--connection_target",
                                     help="Database connection target name (e.g. employee, customer).", metavar="ARG")
            option_parser.add_option("-f", "--display_format", help="Display format (e.g. table, csv).", metavar="ARG")
            option_parser.add_option("-d", "--field_delimiter", help="Delimiter when csv is output (e.g. #&, \\|).",
                                     metavar="ARG")
            option_parser.add_option("-l", "--column_max_length",
                                     help="Maximum width of column when table is output (e.g. 30).", metavar="ARG")
            option_parser.add_option("-e", "--heading", help="Whether to display the header (e.g. on, off).",
                                     metavar="ARG")
            option_parser.add_option("-b", "--feedback", help="Whether to display the result message (e.g. on, off).",
                                     metavar="ARG")
            option_parser.add_option("-p", "--pagesize", help="Number of lines to display per page (e.g. 10).",
                                     metavar="ARG")

            (options, args) = option_parser.parse_args()

            # ---- 起動オプションを元に、コンテキストオブジェクトを設定 ----
            # ---- display_format ----
            if options.display_format:
                self.__context.display_format = options.display_format
            else:
                self.__context.display_format = Context.DisplayFormat.TABLE

            # ---- field_delimiter ----
            if options.field_delimiter:
                self.__context.field_delimiter = options.field_delimiter
            else:
                if self.__context.display_format == Context.DisplayFormat.CSV:
                    self.__context.field_delimiter = ","

            # ---- column_max_length ----
            if options.column_max_length:
                self.__context.column_max_length = int(options.column_max_length)
            else:
                if self.__context.display_format == Context.DisplayFormat.TABLE:
                    self.__context.column_max_length = 1000

            # ---- heading ----
            if options.heading:
                self.__context.heading = options.heading
            else:
                if self.__context.display_format == Context.DisplayFormat.TABLE:
                    self.__context.heading = Context.Heading.ON
                elif self.__context.display_format == Context.DisplayFormat.CSV:
                    self.__context.heading = Context.Heading.OFF

            # ---- feedback ----
            if options.feedback:
                self.__context.feedback = options.feedback
            else:
                if self.__context.display_format == Context.DisplayFormat.TABLE:
                    self.__context.feedback = Context.Feedback.ON
                if self.__context.display_format == Context.DisplayFormat.CSV:
                    self.__context.feedback = Context.Feedback.OFF

            # ---- pagesize ----
            if options.pagesize:
                self.__context.pagesize = int(options.pagesize)
            else:
                if self.__context.display_format == Context.DisplayFormat.TABLE:
                    self.__context.pagesize = 10
                if self.__context.display_format == Context.DisplayFormat.CSV:
                    self.__context.pagesize = 0

            # ---- connection_target ----
            if options.connection_target:
                self.__context.connection_target = options.connection_target
            else:
                self.__context.connection_target = "default"

            # ---- 起動オプションをパースした後の、コンテキストオブジェクトの状態チェック ----
            if not self.__context.check_state_after_parse_option():
                raise OptParseError(u"起動オプションが不正です。")

            # ---- シグナルハンドラーの設定 ----
            signal.signal(signal.SIGINT, self.terminate_subprocess)
            signal.signal(signal.SIGTERM, self.terminate_subprocess)
            if not platform.system() == "Windows":
                signal.signal(signal.SIGHUP, self.terminate_subprocess)
                signal.signal(signal.SIGQUIT, self.terminate_subprocess)

            # ---- データベース固有の処理 ----
            db_type = config.get(self.__context.connection_target, "db_type")

            if db_type == Context.DataBase.ORACLE:
                OracleRunner(config, self.__context).execute()
            elif db_type == Context.DataBase.MYSQL:
                MysqlRunner(config, self.__context).execute()

            self.__logger.info("[End] " + os.path.abspath(__file__))

        except OptParseError as e:
            self.__logger.exception(u"起動オプションが不正です。")
            traceback.print_exc()
            option_parser.print_help()
            sys.exit(1)

        except Exception as e:
            self.__logger.exception(u"想定外のエラーが発生しました。")
            traceback.print_exc()
            sys.exit(1)

    def terminate_subprocess(self):
        # type: () -> None

        for popen in self.__context.subprocesses:  # type: Popen
            if isinstance(popen, Popen):
                if popen.poll() is None:
                    popen.terminate()
