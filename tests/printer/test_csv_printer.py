# coding: utf-8

import unittest
from StringIO import StringIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.printer.csv_printer import CsvPrinter


class TestCsvPrinter(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- パターン1 ----
        context = self._default_context()

        expected = u'''\
ID,NAME,TYPE
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
ID-222-2222,NAME-222-2222,TYPE-222-2222

ID,NAME,TYPE
ID-333-3333,NAME-333-3333,TYPE-333-3333

4行が選択されました。
'''

        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            CsvPrinter(context).execute()
            self.assertEqual(expected, stdout.getvalue().decode("utf-8"))

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.field_delimiter = ","
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
