# coding: utf-8
import os
import sys
import unittest
from io import BytesIO
from unittest import TestCase

import mock

from dbclient.db_client import DbClient


class TestDbClient(TestCase):

    # noinspection PyUnresolvedReferences
    def test_execute(self):
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
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            db_client = DbClient()
            db_client.execute()

            # 検証
            expected = None
            actual = os.environ.get("DBCLIENT_PROFILE")
            self.assertEqual(expected, actual)

            expected = "dbclient/log"
            actual = os.environ.get("LOG_DIR")
            self.assertIn(expected, actual)

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "dbclient"
            actual = db_client._DbClient__context.root_dir
            self.assertIn(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.profile
            self.assertEqual(expected, actual)

            expected = "dbclient/config/default"
            actual = db_client._DbClient__context.config_dir
            self.assertIn(expected, actual)

            expected = "dbclient/log"
            actual = db_client._DbClient__context.log_dir
            self.assertIn(expected, actual)

            expected = "table"
            actual = db_client._DbClient__context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = db_client._DbClient__context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = db_client._DbClient__context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = db_client._DbClient__context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.connection_target
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース2.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = False
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            with self.assertRaises(StandardError) as e:
                db_client = DbClient()
                db_client.execute()

            # 検証
            expected = u"アプリケーションの初期化処理に失敗しました。"
            actual = e.exception.message
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_not_called()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース2.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", "log_dir"), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("log_dir", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            db_client = DbClient()
            db_client.execute()

            # 検証
            expected = None
            actual = os.environ.get("DBCLIENT_PROFILE")
            self.assertEqual(expected, actual)

            expected = "log_dir"
            actual = os.environ.get("LOG_DIR")
            self.assertIn(expected, actual)

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "dbclient"
            actual = db_client._DbClient__context.root_dir
            self.assertIn(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.profile
            self.assertEqual(expected, actual)

            expected = "dbclient/config/default"
            actual = db_client._DbClient__context.config_dir
            self.assertIn(expected, actual)

            expected = "log_dir"
            actual = db_client._DbClient__context.log_dir
            self.assertIn(expected, actual)

            expected = "table"
            actual = db_client._DbClient__context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = db_client._DbClient__context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = db_client._DbClient__context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = db_client._DbClient__context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.connection_target
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース2.2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "mysql")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            db_client = DbClient()
            db_client.execute()

            # 検証
            expected = None
            actual = os.environ.get("DBCLIENT_PROFILE")
            self.assertEqual(expected, actual)

            expected = "dbclient/log"
            actual = os.environ.get("LOG_DIR")
            self.assertIn(expected, actual)

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "dbclient"
            actual = db_client._DbClient__context.root_dir
            self.assertIn(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.profile
            self.assertEqual(expected, actual)

            expected = "dbclient/config/default"
            actual = db_client._DbClient__context.config_dir
            self.assertIn(expected, actual)

            expected = "dbclient/log"
            actual = db_client._DbClient__context.log_dir
            self.assertIn(expected, actual)

            expected = "table"
            actual = db_client._DbClient__context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = db_client._DbClient__context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = db_client._DbClient__context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = db_client._DbClient__context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.connection_target
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_called_once()

        # ---- ケース3.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", False), ("dbclient/log", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            with self.assertRaises(StandardError) as e:
                db_client = DbClient()
                db_client.execute()

            # 検証
            expected = u"環境変数[DBCLIENT_PROFILE]が不正です。DBCLIENT_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" % (
                    db_client._DbClient__context.root_dir + "/config/")
            actual = e.exception.message
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_not_called()
            makedirs.assert_not_called()
            context_check_option_parse.assert_not_called()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース3.2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", True)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            db_client = DbClient()
            db_client.execute()

            # 検証
            expected = None
            actual = os.environ.get("DBCLIENT_PROFILE")
            self.assertEqual(expected, actual)

            expected = "dbclient/log"
            actual = os.environ.get("LOG_DIR")
            self.assertIn(expected, actual)

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "dbclient"
            actual = db_client._DbClient__context.root_dir
            self.assertIn(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.profile
            self.assertEqual(expected, actual)

            expected = "dbclient/config/default"
            actual = db_client._DbClient__context.config_dir
            self.assertIn(expected, actual)

            expected = "dbclient/log"
            actual = db_client._DbClient__context.log_dir
            self.assertIn(expected, actual)

            expected = "table"
            actual = db_client._DbClient__context.display_format
            self.assertEqual(expected, actual)

            expected = ""
            actual = db_client._DbClient__context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 1000
            actual = db_client._DbClient__context.column_max_length
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.heading
            self.assertEqual(expected, actual)

            expected = "on"
            actual = db_client._DbClient__context.feedback
            self.assertEqual(expected, actual)

            expected = 10
            actual = db_client._DbClient__context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.connection_target
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_not_called()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース5.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py", "--display_format", "csv"]

            # 実行
            db_client = DbClient()
            db_client.execute()

            # 検証
            expected = None
            actual = os.environ.get("DBCLIENT_PROFILE")
            self.assertEqual(expected, actual)

            expected = "dbclient/log"
            actual = os.environ.get("LOG_DIR")
            self.assertIn(expected, actual)

            expected = "utf-8"
            actual = os.environ.get("PYTHONIOENCODING")
            self.assertEqual(expected, actual)

            expected = "dbclient"
            actual = db_client._DbClient__context.root_dir
            self.assertIn(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.profile
            self.assertEqual(expected, actual)

            expected = "dbclient/config/default"
            actual = db_client._DbClient__context.config_dir
            self.assertIn(expected, actual)

            expected = "dbclient/log"
            actual = db_client._DbClient__context.log_dir
            self.assertIn(expected, actual)

            expected = "csv"
            actual = db_client._DbClient__context.display_format
            self.assertEqual(expected, actual)

            expected = ","
            actual = db_client._DbClient__context.field_delimiter
            self.assertEqual(expected, actual)

            expected = 0
            actual = db_client._DbClient__context.column_max_length
            self.assertEqual(expected, actual)

            expected = "off"
            actual = db_client._DbClient__context.heading
            self.assertEqual(expected, actual)

            expected = "off"
            actual = db_client._DbClient__context.feedback
            self.assertEqual(expected, actual)

            expected = 0
            actual = db_client._DbClient__context.pagesize
            self.assertEqual(expected, actual)

            expected = "default"
            actual = db_client._DbClient__context.connection_target
            self.assertEqual(expected, actual)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_called_once()
            mysql_runner_execute.assert_not_called()

        # ---- ケース6 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            stderr.encoding = "utf-8"

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            if os.environ.get("PYTHONIOENCODING"):
                del os.environ["PYTHONIOENCODING"]

            sys.argv = ["db_client.py"]

            # 実行
            with self.assertRaises(SystemExit):
                db_client = DbClient()
                db_client.execute()

            # 検証
            expected = u"環境変数\\[PYTHONIOENCODING]がセットされてない、又は不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_not_called()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース7 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            stderr.encoding = "utf-8"

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "euc-jp"
            sys.argv = ["db_client.py"]

            # 実行
            with self.assertRaises(SystemExit):
                db_client = DbClient()
                db_client.execute()

            # 検証
            expected = u"環境変数\\[PYTHONIOENCODING]がセットされてない、又は不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_not_called()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

        # ---- ケース8 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("logging.getLogger"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("dbclient.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("dbclient.context.context.Context.check_option_parse") as context_check_option_parse, \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute, \
                mock.patch("dbclient.runner.mysql_runner.MysqlRunner.execute") as mysql_runner_execute:

            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = False

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""), ("default", "db_type", "oracle")))

            isdir.side_effect = self._isdir_side_effect(
                (("dbclient/config/default", True), ("dbclient/log", False)))

            stderr.encoding = "utf-8"

            if os.environ.get("DBCLIENT_PROFILE"):
                del os.environ["DBCLIENT_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["db_client.py"]

            # 実行
            with self.assertRaises(SystemExit):
                db_client = DbClient()
                db_client.execute()

            # 検証
            expected = u"起動オプションが不正です。"
            actual = stderr.getvalue().decode("utf-8")
            self.assertRegexpMatches(actual, expected)

            context_check_application_initialize.assert_called_once()
            makedirs.assert_called_once()
            context_check_option_parse.assert_called_once()
            oracle_runner_execute.assert_not_called()
            mysql_runner_execute.assert_not_called()

    @staticmethod
    def _isdir_side_effect(return_values):
        # type: (tuple) -> object

        def isdir(inner_path):
            # type: (str) -> bool

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] in inner_path:
                    return return_value_tuple[1]

            raise StandardError(u"引数が不正です。")

        return isdir

    @staticmethod
    def _config_parser_get_side_effect(return_values):
        # type: (tuple) -> object

        def config_parser_get(inner_section, inner_option):
            # type: (str, str) -> str

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] == inner_section and return_value_tuple[1] == inner_option:
                    return return_value_tuple[2]

            raise StandardError(u"引数が不正です。")

        return config_parser_get


if __name__ == "__main__":
    unittest.main()
