# coding: utf-8
import os
import unittest
from unittest import TestCase

import mock

from dbclient.context.context import Context


class TestContext(TestCase):

    def test_check_application_initialize(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = True
            self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), False),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), False),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), False)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = None
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = ""
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("db-client", "dbclient")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "config", "default")), True),
                (os.path.abspath(os.path.join("db-client", "dbclient", "log")), True)))

            context = Context()
            context.profile = 1
            context.root_dir = os.path.abspath(os.path.join("db-client", "dbclient"))
            context.config_dir = os.path.abspath(
                os.path.join("db-client", "dbclient", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("db-client", "dbclient", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

    def test_check_option_parse(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        context = self._default_context()
        context.display_format = "table"

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        context = self._default_context()
        context.display_format = "TABLE"

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = ","

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.4 ----
        context = self._default_context()
        context.display_format = "CSV"
        context.field_delimiter = ","

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = None

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = ""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = u""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = None

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.2 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = ""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.3 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = 0

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース5.1 ----
        context = self._default_context()
        context.heading = "on"

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース5.2 ----
        context = self._default_context()
        context.heading = "ON"

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース5.3 ----
        context = self._default_context()
        context.heading = "off"

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース5.4 ----
        context = self._default_context()
        context.heading = "OFF"

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース6.1 ----
        context = self._default_context()
        context.feedback = "on"

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース6.2 ----
        context = self._default_context()
        context.feedback = "ON"

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース6.3 ----
        context = self._default_context()
        context.feedback = "off"

        actual = context.check_option_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース6.4 ----
        context = self._default_context()
        context.feedback = "OFF"

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース7.1 ----
        context = self._default_context()
        context.pagesize = None

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース7.2 ----
        context = self._default_context()
        context.pagesize = ""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース7.3 ----
        context = self._default_context()
        context.pagesize = -1

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース8.1 ----
        context = self._default_context()
        context.connection_target = None

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース8.2 ----
        context = self._default_context()
        context.connection_target = ""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース8.3 ----
        context = self._default_context()
        context.connection_target = u""

        actual = context.check_option_parse()
        expected = False
        self.assertEqual(expected, actual)

    def test_check_sql_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        actual = context.check_sql_execute()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        context = self._default_context()
        context.subprocesses = None

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        context = self._default_context()
        context.subprocesses = ""

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        context = self._default_context()
        context.subprocesses = ()

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        context = self._default_context()
        context.sql = None

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        context = self._default_context()
        context.sql = u""

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        context = self._default_context()
        context.sql = 1

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        context = self._default_context()
        context.dsn = None

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.2 ----
        context = self._default_context()
        context.dsn = ""

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.3 ----
        context = self._default_context()
        context.dsn = 1

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース5.1 ----
        context = self._default_context()
        context.sql_client_return_code = None

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース5.2 ----
        context = self._default_context()
        context.sql_client_return_code = ""

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース5.3 ----
        context = self._default_context()
        context.sql_client_return_code = "0"

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース6.1 ----
        context = self._default_context()
        context.result_set_html = None

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース6.2 ----
        context = self._default_context()
        context.result_set_html = ""

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース6.3 ----
        context = self._default_context()
        context.result_set_html = 1

        actual = context.check_sql_execute()
        expected = False
        self.assertEqual(expected, actual)

    def test_check_result_set_parse(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        actual = context.check_result_set_parse()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        context = self._default_context()
        context.result_headings = None

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        context = self._default_context()
        context.result_headings = ""

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        context = self._default_context()
        context.result_headings = ()

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        context = self._default_context()
        context.result_sets = None

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        context = self._default_context()
        context.result_sets = ""

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        context = self._default_context()
        context.result_sets = ()

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        context = self._default_context()
        context.result_message = None

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.2 ----
        context = self._default_context()
        context.result_message = ""

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.3 ----
        context = self._default_context()
        context.result_message = 1

        actual = context.check_result_set_parse()
        expected = False
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.root_dir = os.path.dirname(os.path.abspath(__file__))
        context.profile = "test"
        context.config_dir = context.root_dir + "/config/" + context.profile
        context.log_dir = context.root_dir + "/log"
        context.subprocesses.append(mock.MagicMock())
        context.subprocesses.append(mock.MagicMock())
        context.display_format = "table"
        context.field_delimiter = ""
        context.column_max_length = 500
        context.heading = "on"
        context.feedback = "on"
        context.pagesize = 3
        context.connection_target = "default"
        context.sql = u"sql"
        context.dsn = "dsn"
        context.sql_client_return_code = 0
        context.result_set_html = u""
        context.result_headings = ["ID", "NAME", "TYPE"]
        context.result_sets = []
        context.result_sets.append(["ID-000-0000", "NAME-000-0000", "TYPE-000-0000"])
        context.result_sets.append(["ID-111-1111", "NAME-111-1111", "TYPE-111-1111"])
        context.result_sets.append(["ID-222-2222", "NAME-222-2222", "TYPE-222-2222"])
        context.result_sets.append(["ID-333-3333", "NAME-333-3333", "TYPE-333-3333"])
        context.result_message = u"4行が選択されました。"
        return context

    @staticmethod
    def _isdir_side_effect(return_values):
        # type: (tuple) -> object

        def isdir(inner_path):
            # type: (str) -> bool

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] == inner_path:
                    return return_value_tuple[1]

            raise StandardError(u"引数が不正です。")

        return isdir


if __name__ == "__main__":
    unittest.main()
