# coding: utf-8
import os
import unittest
from ConfigParser import SafeConfigParser
from io import BytesIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.runner.oracle_runner import OracleRunner


class TestOracleRunner(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            # 前提条件
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = True

            context = self._default_context()
            context.config = self._default_config()
            config = context.config
            config.set("test", "privilege", "")
            context.display_format = "table"

            # 実行
            OracleRunner(context).execute()

            # 検証
            expected = "oracle_home"
            actual = os.environ.get("ORACLE_HOME")
            self.assertEqual(expected, actual)

            expected = "ld_library_path"
            actual = os.environ.get("LD_LIBRARY_PATH")
            self.assertEqual(expected, actual)

            expected = "nls_lang"
            actual = os.environ.get("NLS_LANG")
            self.assertEqual(expected, actual)

            expected = "nls_date_format"
            actual = os.environ.get("NLS_DATE_FORMAT")
            self.assertEqual(expected, actual)

            expected = "nls_timestamp_format"
            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_called_once()
            csv_printer_execute.assert_not_called()

        # ---- ケース2.1 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            # 前提条件
            context_check_sql_execute.return_value = False
            context_check_result_set_parse.return_value = True

            context = self._default_context()
            context.config = self._default_config()
            config = context.config
            config.set("test", "privilege", "")
            context.display_format = "table"

            # 実行
            with self.assertRaises(StandardError) as e:
                OracleRunner(context).execute()

            # 検証
            self.assertEqual(u"SQLクライアントの実行結果が不正です。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_not_called()
            context_check_result_set_parse.assert_not_called()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース3.1 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            # 前提条件
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = False

            context = self._default_context()
            context.config = self._default_config()
            context.display_format = "table"

            # 実行
            with self.assertRaises(StandardError) as e:
                OracleRunner(context).execute()

            # 検証
            self.assertEqual(u"SQLクライアントの実行結果の、パース処理に失敗しました。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース4.1 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            # 前提条件
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = True

            context = self._default_context()
            context.config = self._default_config()
            config = context.config
            config.set("test", "privilege", "sys")
            context.display_format = "table"

            # 実行
            OracleRunner(context).execute()

            # 検証
            expected = "oracle_home"
            actual = os.environ.get("ORACLE_HOME")
            self.assertEqual(expected, actual)

            expected = "ld_library_path"
            actual = os.environ.get("LD_LIBRARY_PATH")
            self.assertEqual(expected, actual)

            expected = "nls_lang"
            actual = os.environ.get("NLS_LANG")
            self.assertEqual(expected, actual)

            expected = "nls_date_format"
            actual = os.environ.get("NLS_DATE_FORMAT")
            self.assertEqual(expected, actual)

            expected = "nls_timestamp_format"
            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_called_once()
            csv_printer_execute.assert_not_called()

        # ---- ケース5.1 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.oracle_parser.OracleParser.execute") as oracle_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            # 前提条件
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = True

            context = self._default_context()
            context.config = self._default_config()
            context.display_format = "csv"

            # 実行
            OracleRunner(context).execute()

            # 検証
            expected = "oracle_home"
            actual = os.environ.get("ORACLE_HOME")
            self.assertEqual(expected, actual)

            expected = "ld_library_path"
            actual = os.environ.get("LD_LIBRARY_PATH")
            self.assertEqual(expected, actual)

            expected = "nls_lang"
            actual = os.environ.get("NLS_LANG")
            self.assertEqual(expected, actual)

            expected = "nls_date_format"
            actual = os.environ.get("NLS_DATE_FORMAT")
            self.assertEqual(expected, actual)

            expected = "nls_timestamp_format"
            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_called_once()

    @staticmethod
    def _default_config():
        # type: () -> SafeConfigParser

        config = SafeConfigParser()
        config.add_section("oracle_environment_variable")
        config.set("oracle_environment_variable", "oracle_home", "oracle_home")
        config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
        config.set("oracle_environment_variable", "sqlplus_path", "sqlplus_path")
        config.set("oracle_environment_variable", "nls_lang", "nls_lang")
        config.set("oracle_environment_variable", "nls_date_format", "nls_date_format")
        config.set("oracle_environment_variable", "nls_timestamp_format", "nls_timestamp_format")

        config.add_section("test")
        config.set("test", "user_name", "user_name")
        config.set("test", "password", "password")
        config.set("test", "host", "host")
        config.set("test", "port", "port")
        config.set("test", "sid", "sid")
        config.set("test", "privilege", "")
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
