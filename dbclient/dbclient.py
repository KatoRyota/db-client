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
from optparse import OptionParser, OptParseError
from subprocess import Popen

from context.context import Context
from runner.mysql_runner import MysqlRunner
from runner.oracle_runner import OracleRunner

reload(sys)
sys.setdefaultencoding("utf-8")

APP_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
context = Context()
option_parser = OptionParser()

# ---- 設定ファイルの読み込み ----
profile = os.environ.get("DBCLIENT_PROFILE")

if not profile:
    profile = "local"

if not os.path.isdir(APP_ROOT_DIR + "/config/" + os.environ.get("DBCLIENT_PROFILE")):
    raise StandardError(u"環境変数[DBCLIENT_PROFILE]が不正です。DBCLIENT_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" %
                        APP_ROOT_DIR + "/config/")

config = SafeConfigParser()
config.read(APP_ROOT_DIR + "/config/" + os.environ.get("DBCLIENT_PROFILE") + "/application.conf")

if not os.path.isdir("./log"):
    os.makedirs("./log")

logging.config.fileConfig(APP_ROOT_DIR + "/config/" + os.environ.get("DBCLIENT_PROFILE") + "/logging.conf")
logger = logging.getLogger(__name__)


def terminate_subprocess():
    # type: () -> None

    for popen in context.subprocesses:  # type: Popen
        if isinstance(popen, Popen):
            if popen.poll() is None:
                popen.terminate()


def main():
    # noinspection PyBroadException
    try:
        logger.info("[Start] " + os.path.abspath(__file__))

        # ---- 環境変数[PYTHONIOENCODING]のチェック ----
        if os.getenv("PYTHONIOENCODING"):
            if not re.match(r"^utf[\-_]?8$", os.getenv("PYTHONIOENCODING"), re.IGNORECASE):
                raise StandardError(u"環境変数[PYTHONIOENCODING]が不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")
        else:
            raise StandardError(u"環境変数[PYTHONIOENCODING]がセットされていません。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")

        # ---- システム環境情報を出力 ----
        logger.debug("system/OS name -> " + platform.system())
        logger.debug("[encoding] locale -> " + locale.getpreferredencoding())
        logger.debug("[encoding] default -> " + sys.getdefaultencoding())
        logger.debug("[encoding] filesystem -> " + sys.getfilesystemencoding())
        logger.debug("[encoding] stdin -> " + sys.stdin.encoding)
        logger.debug("[encoding] stdout -> " + sys.stdout.encoding)
        logger.debug("[encoding] stderr -> " + sys.stderr.encoding)

        # ---- 起動オプションのパース ----
        option_parser.set_usage("python -m dbclient [-h][-t ARG][-f ARG][-d ARG][-l ARG][-e ARG][-b ARG][-p ARG]")

        option_parser.add_option("-t", "--connection_target",
                                 help="Database connection target name (e.g. employee, customer).", metavar="ARG")
        option_parser.add_option("-f", "--display_format", help="Display format (e.g. table, csv).", metavar="ARG")
        option_parser.add_option("-d", "--field_delimiter", help="Delimiter when csv is output (e.g. #&, \\|).",
                                 metavar="ARG")
        option_parser.add_option("-l", "--column_max_length",
                                 help="Maximum width of column when table is output (e.g. 30).", metavar="ARG")
        option_parser.add_option("-e", "--heading", help="Whether to display the header (e.g. on, off).", metavar="ARG")
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
        signal.signal(signal.SIGINT, terminate_subprocess)
        signal.signal(signal.SIGTERM, terminate_subprocess)
        if not platform.system() == "Windows":
            signal.signal(signal.SIGHUP, terminate_subprocess)
            signal.signal(signal.SIGQUIT, terminate_subprocess)

        # ---- データベース固有の処理 ----
        db_type = config.get(context.connection_target, "db_type")

        if db_type == Context.DataBase.ORACLE:
            OracleRunner(config, context).execute()
        elif db_type == Context.DataBase.MYSQL:
            MysqlRunner(config, context).execute()

        logger.info("[End] " + os.path.abspath(__file__))

    except OptParseError as e:
        logger.exception(u"起動オプションが不正です。")
        traceback.print_exc()
        option_parser.print_help()
        sys.exit(1)

    except Exception as e:
        logger.exception(u"想定外のエラーが発生しました。")
        traceback.print_exc()
        sys.exit(1)
