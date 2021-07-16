# coding: utf-8
import logging
import os
import sys
from ConfigParser import SafeConfigParser
from logging import Logger
from subprocess import Popen, PIPE

from ..context.context import Context
from ..parser.mysql_parser import MysqlParser
from ..printer.csv_printer import CsvPrinter
from ..printer.table_printer import TablePrinter


class MysqlRunner(object):
    __slots__ = (
        "__logger",
        "__config",
        "__context"
    )

    def __init__(self, config, context):
        # type: (SafeConfigParser, Context) -> None

        super(MysqlRunner, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__config = config  # type: SafeConfigParser
        self.__context = context  # type: Context

    def execute(self):
        # type: () -> None

        # ---- 環境変数の設定 ----
        os.environ["MYSQL_PWD"] = self.__config.get(self.__context.connection_target, "password")

        # ---- 環境変数のチェック ----
        if not os.environ["MYSQL_PWD"]:
            raise StandardError(u"環境変数[MYSQL_PWD]がセットされていません。設定ファイルに、値が設定されてない可能性があります。")

        # ---- 標準入力を読み込み ----
        sql = sys.stdin.read().decode("utf-8")

        # ---- mysqlの呼び出し ----
        host = self.__config.get(self.__context.connection_target, "host")
        port = self.__config.get(self.__context.connection_target, "port")
        database_name = self.__config.get(self.__context.connection_target, "database_name")
        user_name = self.__config.get(self.__context.connection_target, "user_name")

        echo_command = ["echo", sql]
        mysql_command = ["mysql", "-h", host, "-P", port, "-D", database_name, "-u", user_name, "--html"]

        self.__logger.debug(u"echo \"%s\" | mysql -h %s -P %s -D %s -u %s --html" %
                            (sql, host, port, database_name, user_name))

        echo_process = Popen(echo_command, stdout=PIPE)
        self.__context.subprocesses.append(echo_process)

        mysql_process = Popen(mysql_command, stdin=echo_process.stdout, stdout=PIPE)
        self.__context.subprocesses.append(mysql_process)

        echo_process.stdout.close()
        result_set_html = mysql_process.communicate()[0].decode("utf-8")
        self.__logger.debug(result_set_html)
        self.__context.sql_client_return_code = mysql_process.returncode
        self.__context.result_set_html = result_set_html

        if not self.__context.check_state_after_execute_sql_client():
            raise StandardError(u"SQLクライアントの実行結果が不正です。")

        # ---- mysqlの呼び出し結果をパース ----
        MysqlParser(self.__context).execute()

        if not self.__context.check_state_after_parse_sql_client_result():
            raise StandardError(u"SQLクライアントの実行結果の、パース処理に失敗しました。")

        # ---- パースした結果を標準出力に出力 ----
        if self.__context.display_format == Context.DisplayFormat.TABLE:
            TablePrinter(self.__context).execute()
        elif self.__context.display_format == Context.DisplayFormat.CSV:
            CsvPrinter(self.__context).execute()
