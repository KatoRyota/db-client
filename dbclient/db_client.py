# coding: utf-8
import locale
import logging.config
import os
import platform
import re
import signal
import sys
import traceback
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

        # ---- アプリケーションの初期化処理 ----
        super(DbClient, self).__init__()
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.__context = Context()  # type: Context
        context = self.__context

        context.root_dir = os.path.dirname(os.path.abspath(__file__))

        context.profile = os.environ.get("DBCLIENT_PROFILE")

        if not context.profile:
            context.profile = "local"

        context.config_dir = context.root_dir + "/config/" + context.profile

        if not os.path.isdir(context.config_dir):
            raise StandardError(u"環境変数[DBCLIENT_PROFILE]が不正です。DBCLIENT_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" %
                                (context.root_dir + "/config/"))

        if not context.check_application_initialize():
            raise StandardError(u"アプリケーションの初期化処理に失敗しました。")

        # ---- ロギング設定ファイルの読み込み ----
        if not os.path.isdir("./log"):
            os.makedirs("./log")

        logging.config.fileConfig(context.config_dir + "/logging.conf")
        self.__logger = logging.getLogger(__name__)  # type: Logger

    @staticmethod
    def main():
        # type: () -> None

        DbClient().execute()

    def execute(self):
        # type: () -> None

        logger = self.__logger
        context = self.__context
        option_parser = OptionParser()

        # noinspection PyBroadException
        try:
            logger.info("[Start] " + os.path.abspath(__file__))

            # ---- アプリケーション設定ファイルの読み込み ----
            config = context.config
            config.read(context.config_dir + "/application.conf")

            if not os.environ.get("PYTHONIOENCODING") or \
                    not re.match(r"^utf[\-_]?8$", os.environ.get("PYTHONIOENCODING"), re.IGNORECASE):
                raise StandardError(u"環境変数[PYTHONIOENCODING]がセットされてない、又は不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")

            # ---- システム環境情報を出力 ----
            logger.debug("system/OS name -> " + platform.system())
            logger.debug("[encoding] locale -> " + locale.getpreferredencoding())
            logger.debug("[encoding] default -> " + sys.getdefaultencoding())
            logger.debug("[encoding] filesystem -> " + sys.getfilesystemencoding())
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stdin -> " + sys.stdin.encoding)
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stdout -> " + sys.stdout.encoding)
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stderr -> " + sys.stderr.encoding)
            logger.debug("アプリケーション設定ファイルパス -> " + context.config_dir + "/application.conf")
            logger.debug("ロギング設定ファイルパス -> " + context.config_dir + "/logging.conf")

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
                context.display_format = options.display_format
            else:
                context.display_format = Context.DisplayFormat.TABLE

            # ---- field_delimiter ----
            if options.field_delimiter:
                context.field_delimiter = options.field_delimiter
            else:
                if context.display_format == Context.DisplayFormat.CSV:
                    context.field_delimiter = ","

            # ---- column_max_length ----
            if options.column_max_length:
                context.column_max_length = int(options.column_max_length)
            else:
                if context.display_format == Context.DisplayFormat.TABLE:
                    context.column_max_length = 1000

            # ---- heading ----
            if options.heading:
                context.heading = options.heading
            else:
                if context.display_format == Context.DisplayFormat.TABLE:
                    context.heading = Context.Heading.ON
                elif context.display_format == Context.DisplayFormat.CSV:
                    context.heading = Context.Heading.OFF

            # ---- feedback ----
            if options.feedback:
                context.feedback = options.feedback
            else:
                if context.display_format == Context.DisplayFormat.TABLE:
                    context.feedback = Context.Feedback.ON
                if context.display_format == Context.DisplayFormat.CSV:
                    context.feedback = Context.Feedback.OFF

            # ---- pagesize ----
            if options.pagesize:
                context.pagesize = int(options.pagesize)
            else:
                if context.display_format == Context.DisplayFormat.TABLE:
                    context.pagesize = 10
                if context.display_format == Context.DisplayFormat.CSV:
                    context.pagesize = 0

            # ---- connection_target ----
            if options.connection_target:
                context.connection_target = options.connection_target
            else:
                context.connection_target = "default"

            # ---- 起動オプションをパースした後の、コンテキストオブジェクトの状態チェック ----
            if not context.check_state_after_parse_option():
                raise OptParseError(u"起動オプションが不正です。")

            # ---- シグナルハンドラーの設定 ----
            signal.signal(signal.SIGINT, self.terminate_subprocess)
            signal.signal(signal.SIGTERM, self.terminate_subprocess)
            if not platform.system() == "Windows":
                signal.signal(signal.SIGHUP, self.terminate_subprocess)
                signal.signal(signal.SIGQUIT, self.terminate_subprocess)

            # ---- データベース固有の処理 ----
            db_type = config.get(context.connection_target, "db_type")

            if db_type == Context.DataBase.ORACLE:
                OracleRunner(context).execute()
            elif db_type == Context.DataBase.MYSQL:
                MysqlRunner(context).execute()

            logger.info("[End] " + os.path.abspath(__file__))

        except OptParseError:
            logger.exception(u"起動オプションが不正です。")
            traceback.print_exc()
            option_parser.print_help()
            sys.exit(1)

        except Exception:
            logger.exception(u"想定外のエラーが発生しました。")
            traceback.print_exc()
            sys.exit(1)

    def terminate_subprocess(self):
        # type: () -> None

        context = self.__context

        for popen in context.subprocesses:  # type: Popen
            if isinstance(popen, Popen):
                if popen.poll() is None:
                    popen.terminate()
