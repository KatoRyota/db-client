# coding: utf-8

import unittest
from ConfigParser import SafeConfigParser
from StringIO import StringIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.runner.oracle_runner import OracleRunner


class TestOracleRunner(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=True) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=True) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            OracleRunner(config, context).execute()

            context_check_state_after_execute_sql_client.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_state_after_parse_sql_client_result.assert_called_once()
            table_printer_execute.assert_called_once()

        # ---- ケース2 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=False) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=True) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            with self.assertRaises(StandardError) as e:
                OracleRunner(config, context).execute()

            self.assertEqual(u"SQLクライアントの実行結果が不正です。", e.exception.message)
            context_check_state_after_execute_sql_client.assert_called_once()
            oracle_parser_execute.assert_not_called()
            context_check_state_after_parse_sql_client_result.assert_not_called()
            table_printer_execute.assert_not_called()

        # ---- ケース3 ----
        with mock.patch("sys.stdin", new=StringIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_state_after_execute_sql_client",
                           return_value=True) as context_check_state_after_execute_sql_client, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_state_after_parse_sql_client_result",
                           return_value=False) as context_check_state_after_parse_sql_client_result, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute:
            config = self._default_config()
            context = self._default_context()

            with self.assertRaises(StandardError) as e:
                OracleRunner(config, context).execute()

            self.assertEqual(u"SQLクライアントの実行結果の、パース処理に失敗しました。", e.exception.message)
            context_check_state_after_execute_sql_client.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_state_after_parse_sql_client_result.assert_called_once()
            table_printer_execute.assert_not_called()

    @staticmethod
    def _default_config():
        # type: () -> SafeConfigParser

        config = SafeConfigParser()
        config.add_section("oracle_environment_variable")
        config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
        config.set("oracle_environment_variable", "sqlplus_path", "sqlplus_path")
        config.set("oracle_environment_variable", "nls_lang", "nls_lang")
        config.set("oracle_environment_variable", "nls_date_format", "nls_date_format")
        config.set("oracle_environment_variable", "nls_timestamp_format", "nls_timestamp_format")

        config.add_section("docker")
        config.set("docker", "user_name", "user_name")
        config.set("docker", "password", "password")
        config.set("docker", "host", "host")
        config.set("docker", "port", "port")
        config.set("docker", "sid", "sid")
        config.set("docker", "privilege", "")
        return config

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.display_format = "table"
        context.connection_target = "docker"
        context.column_max_length = 500
        context.heading = "on"
        context.feedback = "on"
        context.pagesize = 3
        context.sql_client_return_code = 0
        context.result_headings = ["ID", "NAME", "TYPE"]
        context.result_sets = []
        context.result_sets.append(["ID-000-0000", "NAME-000-0000", "TYPE-000-0000"])
        context.result_sets.append(["ID-111-1111", "NAME-111-1111", "TYPE-111-1111"])
        context.result_sets.append(["ID-222-2222", "NAME-222-2222", "TYPE-222-2222"])
        context.result_sets.append(["ID-333-3333", "NAME-333-3333", "TYPE-333-3333"])
        context.result_message = u"4行が選択されました。"
        return context


if __name__ == "__main__":
    unittest.main()
