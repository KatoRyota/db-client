# coding: utf-8
import unittest
from io import BytesIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.printer.csv_printer import CsvPrinter


class TestCsvPrinter(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
ID,NAME,TYPE
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
ID-222-2222,NAME-222-2222,TYPE-222-2222

ID,NAME,TYPE
ID-333-3333,NAME-333-3333,TYPE-333-3333

4行が選択されました。
'''
            self.assertEqual(expected, actual)

        # ---- ケース2 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.result_sets = []
            context.result_sets.append([
                u'あ\nいうえお',
                u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表',
                u'<input type="text" value="<font color="red">&lt;&copy;&amp;'])

            context.result_message = \
                u'あ\nいうえお' \
                u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表' \
                u'<input type="text" value="<font color="red">&lt;&copy;&amp;'

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
ID,NAME,TYPE
あ\\nいうえお,," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表,<input type="text" value="<font color="red">&lt;&copy;&amp;

あ
いうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表<input type="text" value="<font color="red">&lt;&copy;&amp;
'''
            self.assertEqual(expected, actual)

        # ---- ケース3 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.result_headings = []
            context.result_sets = []

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\

4行が選択されました。
'''
            self.assertEqual(expected, actual)

        # ---- ケース4 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.result_message = u''

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
ID,NAME,TYPE
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
ID-222-2222,NAME-222-2222,TYPE-222-2222

ID,NAME,TYPE
ID-333-3333,NAME-333-3333,TYPE-333-3333
'''
            self.assertEqual(expected, actual)

        # ---- ケース5 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.heading = "off"

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
ID-222-2222,NAME-222-2222,TYPE-222-2222

ID-333-3333,NAME-333-3333,TYPE-333-3333

4行が選択されました。
'''
            self.assertEqual(expected, actual)

        # ---- ケース6 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.feedback = "off"

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
ID,NAME,TYPE
ID-000-0000,NAME-000-0000,TYPE-000-0000
ID-111-1111,NAME-111-1111,TYPE-111-1111
ID-222-2222,NAME-222-2222,TYPE-222-2222

ID,NAME,TYPE
ID-333-3333,NAME-333-3333,TYPE-333-3333
'''
            self.assertEqual(expected, actual)

        # ---- ケース7 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            context = self._default_context()
            context.sql_client_return_code = 1
            context.result_message = u"予期せぬ例外が発生しました。"

            CsvPrinter(context).execute()

            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
予期せぬ例外が発生しました。
'''
            self.assertEqual(expected, actual)

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
