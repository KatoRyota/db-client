# coding: utf-8
import logging
import os
import sys
from logging import Logger
from subprocess import Popen, PIPE, STDOUT

from ..context.context import Context
from ..parser.oracle_parser import OracleParser
from ..printer.csv_printer import CsvPrinter
from ..printer.table_printer import TablePrinter


class OracleRunner(object):
    __slots__ = (
        "__logger",
        "__context"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(OracleRunner, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context

    def execute(self):
        # type: () -> None

        logger = self.__logger
        context = self.__context
        config = self.__context.config

        # ---- 環境変数の設定 ----
        os.environ["ORACLE_HOME"] = config.get("oracle_environment_variable", "oracle_home")
        os.environ["LD_LIBRARY_PATH"] = config.get("oracle_environment_variable", "ld_library_path")
        os.environ["PATH"] = config.get("oracle_environment_variable", "sqlplus_path") + ":" + os.environ.get("PATH")
        os.environ["NLS_LANG"] = config.get("oracle_environment_variable", "nls_lang")
        os.environ["NLS_DATE_FORMAT"] = config.get("oracle_environment_variable", "nls_date_format")
        os.environ["NLS_TIMESTAMP_FORMAT"] = config.get("oracle_environment_variable", "nls_timestamp_format")

        if not os.environ.get("ORACLE_HOME"):
            raise StandardError(u"環境変数[ORACLE_HOME]が不正です。設定ファイルを確認して下さい。")

        if not os.environ.get("LD_LIBRARY_PATH"):
            raise StandardError(u"環境変数[LD_LIBRARY_PATH]が不正です。設定ファイルを確認して下さい。")

        if not os.environ.get("NLS_LANG"):
            raise StandardError(u"環境変数[NLS_LANG]が不正です。設定ファイルを確認して下さい。")

        if not os.environ.get("NLS_DATE_FORMAT"):
            raise StandardError(u"環境変数[NLS_DATE_FORMAT]が不正です。設定ファイルを確認して下さい。")

        if not os.environ.get("NLS_TIMESTAMP_FORMAT"):
            raise StandardError(u"環境変数[NLS_TIMESTAMP_FORMAT]が不正です。設定ファイルを確認して下さい。")

        # ---- 標準入力の読み込み ----
        context.sql = sys.stdin.read().decode("utf-8")

        # ---- sqlplusの実行 ----
        context.sql = u"\n".join((
            "WHENEVER SQLERROR EXIT 1", "WHENEVER OSERROR EXIT 1", "SET WRAP OFF", "SET LINESIZE 32767",
            "SET LONG 2000000000", "SET LONGCHUNKSIZE 1000", "SET NUMWIDTH 50", "SET TRIMOUT ON", "SET PAGESIZE 50000",
            "SET HEADING ON", "SET FEEDBACK ON", "SET DEFINE OFF", "SET NULL 'NULL'", context.sql))

        context.dsn = "{user_name}/{password}@{host}:{port}/{sid}".format(
            user_name=config.get(context.connection_target, "user_name"),
            password=config.get(context.connection_target, "password"),
            host=config.get(context.connection_target, "host"),
            port=config.get(context.connection_target, "port"),
            sid=config.get(context.connection_target, "sid"))

        privilege = config.get(context.connection_target, "privilege")

        if privilege:
            context.dsn += " AS " + privilege

        echo_command = ["echo", context.sql]
        sqlplus_command = ["sqlplus", "-s", "-M", "HTML ON", context.dsn]

        logger.debug(u"echo \"%s\" | sqlplus -s -M HTML ON \"%s\"" % (context.sql, context.dsn))

        echo_process = Popen(echo_command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(echo_process)

        sqlplus_process = Popen(sqlplus_command, stdin=echo_process.stdout, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(sqlplus_process)

        echo_process.stdout.close()
        result_set_html = sqlplus_process.communicate()[0].decode("utf-8")
        logger.debug(result_set_html)
        context.sql_client_return_code = sqlplus_process.returncode
        context.result_set_html = result_set_html

        if not context.check_sql_execute():
            raise StandardError(u"sqlplusの実行に失敗しました。")

        # ---- sqlplusの実行結果のパース ----
        OracleParser(context).execute()

        if not context.check_result_set_parse():
            raise StandardError(u"sqlplusの実行結果のパースに失敗しました。")

        # ---- sqlplusの実行結果の出力 ----
        if context.display_format == Context.DisplayFormat.TABLE:
            TablePrinter(context).execute()
        elif context.display_format == Context.DisplayFormat.CSV:
            CsvPrinter(context).execute()
