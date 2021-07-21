# coding: utf-8

import unittest
from unittest import TestCase

import mock

from dbclient.context.context import Context


class TestContext(TestCase):

    def test_check_state_after_parse_option(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        expected = True
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース2 ----
        context = self._default_context()
        context.display_format = "json"

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース3 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = ""

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース4 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = None

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース5 ----
        context = self._default_context()
        context.display_format = "csv"
        context.field_delimiter = u""

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース6 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = ""

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース7 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = None

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース9 ----
        context = self._default_context()
        context.display_format = "table"
        context.column_max_length = 0

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース10 ----
        context = self._default_context()
        context.heading = "ON"

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース11 ----
        context = self._default_context()
        context.feedback = "OFF"

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース12 ----
        context = self._default_context()
        context.pagesize = ""

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース13 ----
        context = self._default_context()
        context.pagesize = None

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

        # ---- ケース14 ----
        context = self._default_context()
        context.pagesize = -1

        expected = False
        actual = context.check_state_after_parse_option()
        self.assertEqual(expected, actual)

    def test_check_state_after_execute_sql_client(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        expected = True
        actual = context.check_state_after_execute_sql_client()
        self.assertEqual(expected, actual)

    def test_check_state_after_parse_sql_client_result(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()

        expected = True
        actual = context.check_state_after_parse_sql_client_result()
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.subprocesses.append(mock.MagicMock())
        context.subprocesses.append(mock.MagicMock())
        context.display_format = "table"
        context.field_delimiter = ""
        context.column_max_length = 500
        context.heading = "on"
        context.feedback = "on"
        context.pagesize = 3
        context.connection_target = "default"
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


if __name__ == "__main__":
    unittest.main()
