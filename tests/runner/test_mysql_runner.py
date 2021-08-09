# coding: utf-8
import os
import unittest
from ConfigParser import SafeConfigParser
from io import BytesIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.runner.mysql_runner import MysqlRunner


class TestMysqlRunner(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
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

            config.set("test", "password", "password")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            MysqlRunner(context).execute()

            # 検証
            actual = os.environ.get("MYSQL_PWD")
            expected = "password"
            self.assertEqual(expected, actual)

            actual = context.sql
            expected = u"""\
select * from test;
"""
            self.assertEqual(expected, actual)

            actual = context.dsn
            expected = "-h host -P port -D database_name -u user_name"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_called_once()
            csv_printer_execute.assert_not_called()

        # ---- ケース5.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
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

            config.set("test", "password", "password")

            context.display_format = "csv"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            MysqlRunner(context).execute()

            # 検証
            actual = os.environ.get("MYSQL_PWD")
            expected = "password"
            self.assertEqual(expected, actual)

            actual = context.sql
            expected = u"""\
select * from test;
"""
            self.assertEqual(expected, actual)

            actual = context.dsn
            expected = "-h host -P port -D database_name -u user_name"
            self.assertEqual(expected, actual)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_called_once()

        # ---- ケース2.1 ----
        with mock.patch("sys.stdin", new=BytesIO()) as stdin, \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
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

            config.set("test", "password", "password")

            context.display_format = "table"

            stdin.write("select * from test;\n")
            stdin.seek(0)

            # 実行
            with self.assertRaises(StandardError) as e:
                MysqlRunner(context).execute()

            # 検証
            self.assertEqual(u"SQLクライアントの実行結果が不正です。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_not_called()
            context_check_result_set_parse.assert_not_called()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース4 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            context_check_sql_execute.return_value = False
            context_check_result_set_parse.return_value = True

            context = self._default_context()
            context.config = self._default_config()
            context.display_format = "csv"

            with self.assertRaises(StandardError) as e:
                MysqlRunner(context).execute()

            self.assertEqual(u"SQLクライアントの実行結果が不正です。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_not_called()
            context_check_result_set_parse.assert_not_called()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース5 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = False

            context = self._default_context()
            context.config = self._default_config()
            context.display_format = "table"

            with self.assertRaises(StandardError) as e:
                MysqlRunner(context).execute()

            self.assertEqual(u"SQLクライアントの実行結果の、パース処理に失敗しました。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

        # ---- ケース6 ----
        with mock.patch("sys.stdin", new=BytesIO()), \
                mock.patch("subprocess.Popen.__new__"), \
                mock.patch("dbclient.context.context.Context.check_sql_execute") as context_check_sql_execute, \
                mock.patch("dbclient.parser.mysql_parser.MysqlParser.execute") as mysql_parser_execute, \
                mock.patch("dbclient.context.context.Context.check_result_set_parse"
                           ) as context_check_result_set_parse, \
                mock.patch("dbclient.printer.table_printer.TablePrinter.execute") as table_printer_execute, \
                mock.patch("dbclient.printer.csv_printer.CsvPrinter.execute") as csv_printer_execute:
            context_check_sql_execute.return_value = True
            context_check_result_set_parse.return_value = False

            context = self._default_context()
            context.config = self._default_config()
            context.display_format = "csv"

            with self.assertRaises(StandardError) as e:
                MysqlRunner(context).execute()

            self.assertEqual(u"SQLクライアントの実行結果の、パース処理に失敗しました。", e.exception.message)

            context_check_sql_execute.assert_called_once()
            mysql_parser_execute.assert_called_once()
            context_check_result_set_parse.assert_called_once()
            table_printer_execute.assert_not_called()
            csv_printer_execute.assert_not_called()

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
