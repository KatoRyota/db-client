# coding: utf-8

import unittest
from ConfigParser import SafeConfigParser
from StringIO import StringIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.runner.mysql_runner import MysqlRunner


class TestMysqlRunner(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=True) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=True) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            MysqlRunner(config, context).execute()

            context_check_state_after_execute_sql_client.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_state_after_parse_sql_client_result.assert_called_once()
            table_printer_execute.assert_called_once()

        # ---- ケース2 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=False) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=True) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            with self.assertRaises(StandardError) as e:
                MysqlRunner(config, context).execute()

            self.assertEqual(u"SQLクライアントの実行結果が不正です。", e.exception.message)
            context_check_state_after_execute_sql_client.assert_called_once()
            mysql_parser_execute.assert_not_called()
            context_check_state_after_parse_sql_client_result.assert_not_called()
            table_printer_execute.assert_not_called()

        # ---- ケース3 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=True) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=False) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            with self.assertRaises(StandardError) as e:
                MysqlRunner(config, context).execute()

            self.assertEqual(u"SQLクライアントの実行結果の、パース処理に失敗しました。", e.exception.message)
            context_check_state_after_execute_sql_client.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_state_after_parse_sql_client_result.assert_called_once()
            table_printer_execute.assert_not_called()

    @staticmethod
    def _default_config():
        # type: () -> SafeConfigParser

        config = SafeConfigParser()
        config.add_section("test")
        config.set("test", "user_name", "user_name")
        config.set("test", "password", "password")
        config.set("test", "host", "host")
        config.set("test", "port", "port")
        config.set("test", "database_name", "database_name")
        return config

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.display_format = "table"
        context.connection_target = "test"
        return context


if __name__ == "__main__":
    unittest.main()
