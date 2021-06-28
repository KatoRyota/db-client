# coding: utf-8
import logging
import os
import sys
from ConfigParser import SafeConfigParser
from logging import Logger
from subprocess import Popen, PIPE

from ..context.context import Context
from ..parser.oracle_parser import OracleParser
from ..printer.csv_printer import CsvPrinter
from ..printer.table_printer import TablePrinter


class OracleRunner(object):
    __slots__ = (
        "__logger",
        "__config",
        "__context"
    )

    def __init__(self, config, context):
        # type: (SafeConfigParser, Context) -> None

        super(OracleRunner, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__config = config  # type: SafeConfigParser
        self.__context = context  # type: Context

    def execute(self):
        # type: () -> None

        # ---- 環境変数の設定 ----
        os.environ["LD_LIBRARY_PATH"] = self.__config.get("oracle_environment_variable", "ld_library_path")
        os.environ["PATH"] = self.__config.get("oracle_environment_variable", "sqlplus_path") + ":" + os.environ.get(
            "PATH")
        os.environ["NLS_LANG"] = self.__config.get("oracle_environment_variable", "nls_lang")
        os.environ["NLS_DATE_FORMAT"] = self.__config.get("oracle_environment_variable", "nls_date_format")
        os.environ["NLS_TIMESTAMP_FORMAT"] = self.__config.get("oracle_environment_variable", "nls_timestamp_format")

        # ---- 環境変数のチェック ----
        if not os.environ["LD_LIBRARY_PATH"]:
            raise StandardError(u"環境変数[LD_LIBRARY_PATH]がセットされていません。設定ファイルに、値が設定されてない可能性があります。")

        if not os.environ["NLS_LANG"]:
            raise StandardError(u"環境変数[NLS_LANG]がセットされていません。設定ファイルに、値が設定されてない可能性があります。")

        if not os.environ["NLS_DATE_FORMAT"]:
            raise StandardError(u"環境変数[NLS_DATE_FORMAT]がセットされていません。設定ファイルに、値が設定されてない可能性があります。")

        if not os.environ["NLS_TIMESTAMP_FORMAT"]:
            raise StandardError(u"環境変数[NLS_TIMESTAMP_FORMAT]がセットされていません。設定ファイルに、値が設定されてない可能性があります。")

        # ---- 標準入力を読み込み ----
        sql = sys.stdin.read().decode("utf-8")

        # ---- sqlplusの呼び出し ----
        sql = u"\n".join(("WHENEVER SQLERROR EXIT 1", "WHENEVER OSERROR EXIT 1", "SET WRAP OFF", "SET LINESIZE 32767",
                          "SET LONG 2000000000", "SET LONGCHUNKSIZE 1000", "SET NUMWIDTH 50", "SET TRIMOUT ON",
                          "SET PAGESIZE 50000", "SET HEADING ON", " SET FEEDBACK ON", "SET DEFINE OFF",
                          "SET NULL 'NULL'", sql))

        dsn = "{user_name}/{password}@{host}:{port}/{sid}".format(
            user_name=self.__config.get(self.__context.connection_target, "user_name"),
            password=self.__config.get(self.__context.connection_target, "password"),
            host=self.__config.get(self.__context.connection_target, "host"),
            port=self.__config.get(self.__context.connection_target, "port"),
            sid=self.__config.get(self.__context.connection_target, "sid")
        )

        privilege = self.__config.get(self.__context.connection_target, "privilege")

        if privilege:
            dsn += " AS " + privilege

        echo_command = ["echo", sql]
        sqlplus_command = ["sqlplus", "-s", "-M", "HTML ON", dsn]

        self.__logger.debug(u"echo \"%s\" | sqlplus -s -M HTML ON \"%s\"" % (sql, dsn))

        echo_process = Popen(echo_command, stdout=PIPE)
        self.__context.subprocesses.append(echo_process)

        sqlplus_process = Popen(sqlplus_command, stdin=echo_process.stdout, stdout=PIPE)
        self.__context.subprocesses.append(sqlplus_process)

        echo_process.stdout.close()
        result_set_html = sqlplus_process.communicate()[0].decode("utf-8")
        self.__logger.debug(result_set_html)
        self.__context.sql_client_return_code = sqlplus_process.returncode
        self.__context.result_set_html = result_set_html

        if not self.__context.check_state_after_execute_sql_client():
            raise StandardError(u"SQLクライアントの実行結果が不正です。")

        # ---- sqlplusの呼び出し結果をパース ----
        OracleParser(self.__context).execute()

        if not self.__context.check_state_after_parse_sql_client_result():
            raise StandardError(u"SQLクライアントの実行結果の、パース処理に失敗しました。")

        # ---- パースした結果を標準出力に出力 ----
        if self.__context.display_format == Context.DisplayFormat.TABLE:
            TablePrinter(self.__context).execute()
        elif self.__context.display_format == Context.DisplayFormat.CSV:
            CsvPrinter(self.__context).execute()
