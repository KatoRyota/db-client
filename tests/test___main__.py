# coding: utf-8

import os
import sys
import unittest
from io import BytesIO
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

        # ---- ケース1 ----
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
            config_parser_get.side_effect = self._config_parser_get_side_effect("default", "db_type", "oracle")
            isdir.side_effect = self._isdir_side_effect("./log", False)

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

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
            context_check_state_after_parse_option.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

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
            config_parser_get.side_effect = self._config_parser_get_side_effect("default", "db_type", "mysql")
            isdir.side_effect = self._isdir_side_effect("./log", False)

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

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
            context_check_state_after_parse_option.assert_called_once()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_called_once()

        # ---- ケース3 ----
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
            config_parser_get.side_effect = self._config_parser_get_side_effect("default", "db_type", "oracle")
            isdir.side_effect = self._isdir_side_effect("./log", False)

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + ["--display_format", "csv"]

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

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

            makedirs.assert_called_once()
            context_check_state_after_parse_option.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース4 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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
            config_parser_get.side_effect = self._config_parser_get_side_effect("default", "db_type", "oracle")
            isdir.side_effect = self._isdir_side_effect("./log", True)
            stderr.encoding = "utf-8"

            if os.environ.get("PYTHONIOENCODING"):
                del os.environ["PYTHONIOENCODING"]
            sys.argv = sys.argv + []

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            with self.assertRaises(SystemExit):
                # noinspection PyUnresolvedReferences
                import dbclient.__main__

            expected = u"環境変数\\[PYTHONIOENCODING]がセットされていません。PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            makedirs.assert_not_called()
            context_check_state_after_parse_option.assert_not_called()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース5 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            context_check_state_after_parse_option.return_value = False
            config_parser_get.side_effect = self._config_parser_get_side_effect("default", "db_type", "oracle")
            isdir.side_effect = self._isdir_side_effect("./log", True)
            stderr.encoding = "utf-8"

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = sys.argv + []

            if "dbclient.__main__" in sys.modules:
                del sys.modules["dbclient.__main__"]

            with self.assertRaises(SystemExit):
                # noinspection PyUnresolvedReferences
                import dbclient.__main__

            expected = u"起動オプションが不正です。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            makedirs.assert_not_called()
            context_check_state_after_parse_option.assert_called_once()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

    @staticmethod
    def _isdir_side_effect(path, return_value):
        # type: (str, bool) -> object

        def isdir(inner_path):
            # type: (str) -> bool

            if inner_path == path:
                return return_value
            else:
                raise StandardError(u"引数が不正です。")

        return isdir

    @staticmethod
    def _config_parser_get_side_effect(section, option, return_value):
        # type: (str, str, str) -> object

        def config_parser_get(inner_section, inner_option):
            # type: (str, str) -> str

            if inner_section == section and inner_option == option:
                return return_value
            else:
                raise StandardError(u"引数が不正です。")

        return config_parser_get


if __name__ == "__main__":
    unittest.main()
