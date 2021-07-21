# coding: utf-8

import os
import sys
import unittest
from StringIO import StringIO
from unittest import TestCase

import mock


class TestMain(TestCase):

    def test__main__(self):
        # type: () -> None

        before_stdin = sys.stdin
        before_stdout = sys.stdout
        before_stderr = sys.stderr
        before_argv = sys.argv

        reload(sys)
        sys.setdefaultencoding("utf-8")
        sys.stdin = before_stdin
        sys.stdout = before_stdout
        sys.stderr = before_stderr
        sys.argv = before_argv

        # ---- ケース2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context."
                           "Context.check_state_after_parse_option") as context_check_state_after_parse_option, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            context_check_state_after_parse_option.return_value = True
            config_parser_get.side_effect = self.config_parser_get_oracle_side_effect
            isdir.return_value = False

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            import dbclient.__main__

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "table"
            actual = dbclient.__main__.context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = dbclient.__main__.context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = dbclient.__main__.context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = dbclient.__main__.context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = dbclient.__main__.context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = dbclient.__main__.context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = dbclient.__main__.context.connection_target
            self.assertEqual(expected, actual)

            makedirs.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース3 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.makedirs"), \
                mock.patch("dbclient.context.context."
                           "Context.check_state_after_parse_option") as context_check_state_after_parse_option, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            context_check_state_after_parse_option.return_value = True
            config_parser_get.side_effect = self.config_parser_get_mysql_side_effect

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            import dbclient.__main__

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "table"
            actual = dbclient.__main__.context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = dbclient.__main__.context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = dbclient.__main__.context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = dbclient.__main__.context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = dbclient.__main__.context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = dbclient.__main__.context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = dbclient.__main__.context.connection_target
            self.assertEqual(expected, actual)

            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_called_once()

        # ---- ケース4 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.makedirs"), \
                mock.patch("dbclient.context.context."
                           "Context.check_state_after_parse_option") as context_check_state_after_parse_option, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            context_check_state_after_parse_option.return_value = True
            config_parser_get.side_effect = self.config_parser_get_oracle_side_effect

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + ["--display_format", "csv"]

            import dbclient.__main__

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "csv"
            actual = dbclient.__main__.context.display_format
            self.assertEqual(expected, actual)

            expected = ","
            actual = dbclient.__main__.context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 0
            actual = dbclient.__main__.context.column_max_length
            self.assertEqual(expected, actual)

            expected = "off"
            actual = dbclient.__main__.context.heading
            self.assertEqual(expected, actual)

            expected = "off"
            actual = dbclient.__main__.context.feedback
            self.assertEqual(expected, actual)

            expected = 0
            actual = dbclient.__main__.context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = dbclient.__main__.context.connection_target
            self.assertEqual(expected, actual)

            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=StringIO()) as stderr, \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.makedirs"), \
                mock.patch("dbclient.context.context."
                           "Context.check_state_after_parse_option") as context_check_state_after_parse_option, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            context_check_state_after_parse_option.return_value = True
            config_parser_get.side_effect = self.config_parser_get_oracle_side_effect
            stderr.encoding = "utf-8"

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            if os.environ.get("PYTHONIOENCODING"):
                del os.environ["PYTHONIOENCODING"]
            sys.argv = sys.argv + []

            with self.assertRaises(SystemExit):
                # noinspection PyUnresolvedReferences
                import dbclient.__main__

            expected = u"環境変数\\[PYTHONIOENCODING]がセットされていません。PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース1-2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=StringIO()) as stderr, \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.makedirs"), \
                mock.patch("dbclient.context.context."
                           "Context.check_state_after_parse_option") as context_check_state_after_parse_option, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            context_check_state_after_parse_option.return_value = False
            config_parser_get.side_effect = self.config_parser_get_oracle_side_effect
            stderr.encoding = "utf-8"

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            with self.assertRaises(SystemExit):
                # noinspection PyUnresolvedReferences
                import dbclient.__main__

            expected = u"起動オプションが不正です。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

    @staticmethod
    def config_parser_get_oracle_side_effect(section, option):
        # type: (str, str) -> str

        if section == "default" and option == "db_type":
            return "oracle"
        else:
            return ""

    @staticmethod
    def config_parser_get_mysql_side_effect(section, option):
        # type: (str, str) -> str

        if section == "default" and option == "db_type":
            return "mysql"
        else:
            return ""


if __name__ == "__main__":
    unittest.main()
