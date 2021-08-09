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
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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

            config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
            config.set("test", "privilege", "")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            OracleRunner(context).execute()

            # 検証
            actual = os.environ.get("ORACLE_HOME")
            expected = "oracle_home"
            self.assertEqual(expected, actual)

            actual = os.environ.get("LD_LIBRARY_PATH")
            expected = "ld_library_path"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_LANG")
            expected = "nls_lang"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_DATE_FORMAT")
            expected = "nls_date_format"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            expected = "nls_timestamp_format"
            self.assertEqual(expected, actual)

            actual = context.sql
            expected = u"""\
WHENEVER SQLERROR EXIT 1
WHENEVER OSERROR EXIT 1
SET WRAP OFF
SET LINESIZE 32767
SET LONG 2000000000
SET LONGCHUNKSIZE 1000
SET NUMWIDTH 50
SET TRIMOUT ON
SET PAGESIZE 50000
SET HEADING ON
SET FEEDBACK ON
SET DEFINE OFF
SET NULL 'NULL'
select * from test;
"""
            self.assertEqual(expected, actual)

            actual = context.dsn
            expected = "user_name/password@host:port/sid"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_called_once()
            csv_printer_execute.assert_not_called()

        # ---- ケース2.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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

            config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
            config.set("test", "privilege", "")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            with self.assertRaises(StandardError) as e:
                OracleRunner(context).execute()

            # 検証
            actual = e.exception.message
            expected = u"SQLクライアントの実行結果が不正です。"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_not_called()
            context_check_result_set_parse.assert_not_called()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース3.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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
            config = context.config

            config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
            config.set("test", "privilege", "")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            with self.assertRaises(StandardError) as e:
                OracleRunner(context).execute()

            # 検証
            actual = u"SQLクライアントの実行結果の、パース処理に失敗しました。"
            expected = e.exception.message
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース4.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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

            config.set("oracle_environment_variable", "ld_library_path", "")
            config.set("test", "privilege", "")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            with self.assertRaises(StandardError) as e:
                OracleRunner(context).execute()

            # 検証
            actual = e.exception.message
            expected = u"環境変数[LD_LIBRARY_PATH]がセットされていません。設定ファイルに、値が設定されてない可能性があります。"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_not_called()
            oracle_parser_execute.assert_not_called()
            context_check_result_set_parse.assert_not_called()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース4.2 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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

            config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
            config.set("test", "privilege", "sys")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            OracleRunner(context).execute()

            # 検証
            actual = os.environ.get("ORACLE_HOME")
            expected = "oracle_home"
            self.assertEqual(expected, actual)

            actual = os.environ.get("LD_LIBRARY_PATH")
            expected = "ld_library_path"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_LANG")
            expected = "nls_lang"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_DATE_FORMAT")
            expected = "nls_date_format"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            expected = "nls_timestamp_format"
            self.assertEqual(expected, actual)

            actual = context.sql
            expected = u"""\
WHENEVER SQLERROR EXIT 1
WHENEVER OSERROR EXIT 1
SET WRAP OFF
SET LINESIZE 32767
SET LONG 2000000000
SET LONGCHUNKSIZE 1000
SET NUMWIDTH 50
SET TRIMOUT ON
SET PAGESIZE 50000
SET HEADING ON
SET FEEDBACK ON
SET DEFINE OFF
SET NULL 'NULL'
select * from test;
"""
            self.assertEqual(expected, actual)

            actual = context.dsn
            expected = "user_name/password@host:port/sid AS sys"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            oracle_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_called_once()
            csv_printer_execute.assert_not_called()

        # ---- ケース5.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
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

            config.set("oracle_environment_variable", "ld_library_path", "ld_library_path")
            config.set("test", "privilege", "")

            context.display_format = "csv"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            OracleRunner(context).execute()

            # 検証
            actual = os.environ.get("ORACLE_HOME")
            expected = "oracle_home"
            self.assertEqual(expected, actual)

            actual = os.environ.get("LD_LIBRARY_PATH")
            expected = "ld_library_path"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_LANG")
            expected = "nls_lang"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_DATE_FORMAT")
            expected = "nls_date_format"
            self.assertEqual(expected, actual)

            actual = os.environ.get("NLS_TIMESTAMP_FORMAT")
            expected = "nls_timestamp_format"
            self.assertEqual(expected, actual)

            actual = context.sql
            expected = u"""\
WHENEVER SQLERROR EXIT 1
WHENEVER OSERROR EXIT 1
SET WRAP OFF
SET LINESIZE 32767
SET LONG 2000000000
SET LONGCHUNKSIZE 1000
SET NUMWIDTH 50
SET TRIMOUT ON
SET PAGESIZE 50000
SET HEADING ON
SET FEEDBACK ON
SET DEFINE OFF
SET NULL 'NULL'
select * from test;
"""
            self.assertEqual(expected, actual)

            actual = context.dsn
            expected = "user_name/password@host:port/sid"
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
