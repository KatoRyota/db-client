# coding: utf-8

import unittest
from StringIO import StringIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.printer.table_printer import TablePrinter


class TestTablePrinter(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- パターン1 ----
        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            context = self._default_context()

            TablePrinter(context).execute()

            expected = u'''\
+-----------+-------------+-------------+
|ID         |NAME         |TYPE         |
+-----------+-------------+-------------+
|ID-000-0000|NAME-000-0000|TYPE-000-0000|
+-----------+-------------+-------------+
|ID-111-1111|NAME-111-1111|TYPE-111-1111|
+-----------+-------------+-------------+
|ID-222-2222|NAME-222-2222|TYPE-222-2222|
+-----------+-------------+-------------+

+-----------+-------------+-------------+
|ID         |NAME         |TYPE         |
+-----------+-------------+-------------+
|ID-333-3333|NAME-333-3333|TYPE-333-3333|
+-----------+-------------+-------------+

4行が選択されました。
'''
            actual = stdout.getvalue().decode("utf-8")
            self.assertEqual(expected, actual)

        # ---- パターン2 ----
        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
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

            TablePrinter(context).execute()

            expected = u'''\
+------------+--------------------------------------------------------------------------------------+-----------------------------------------------------------+
|ID          |NAME                                                                                  |TYPE                                                       |
+------------+--------------------------------------------------------------------------------------+-----------------------------------------------------------+
|あ\\nいうえお|," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表|<input type="text" value="<font color="red">&lt;&copy;&amp;|
+------------+--------------------------------------------------------------------------------------+-----------------------------------------------------------+

あ
いうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表<input type="text" value="<font color="red">&lt;&copy;&amp;
'''
            actual = stdout.getvalue().decode("utf-8")
            self.assertEqual(expected, actual)

        # ---- パターン3 ----
        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            context = self._default_context()
            context.heading = "off"

            TablePrinter(context).execute()

            expected = u'''\
+-----------+-------------+-------------+
|ID-000-0000|NAME-000-0000|TYPE-000-0000|
+-----------+-------------+-------------+
|ID-111-1111|NAME-111-1111|TYPE-111-1111|
+-----------+-------------+-------------+
|ID-222-2222|NAME-222-2222|TYPE-222-2222|
+-----------+-------------+-------------+

+-----------+-------------+-------------+
|ID-333-3333|NAME-333-3333|TYPE-333-3333|
+-----------+-------------+-------------+

4行が選択されました。
'''
            actual = stdout.getvalue().decode("utf-8")
            self.assertEqual(expected, actual)

        # ---- パターン4 ----
        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            context = self._default_context()
            context.feedback = "off"

            TablePrinter(context).execute()

            expected = u'''\
+-----------+-------------+-------------+
|ID         |NAME         |TYPE         |
+-----------+-------------+-------------+
|ID-000-0000|NAME-000-0000|TYPE-000-0000|
+-----------+-------------+-------------+
|ID-111-1111|NAME-111-1111|TYPE-111-1111|
+-----------+-------------+-------------+
|ID-222-2222|NAME-222-2222|TYPE-222-2222|
+-----------+-------------+-------------+

+-----------+-------------+-------------+
|ID         |NAME         |TYPE         |
+-----------+-------------+-------------+
|ID-333-3333|NAME-333-3333|TYPE-333-3333|
+-----------+-------------+-------------+
'''
            actual = stdout.getvalue().decode("utf-8")
            self.assertEqual(expected, actual)

        # ---- パターン5 ----
        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            context = self._default_context()
            context.sql_client_return_code = 1
            context.result_message = u"予期せぬ例外が発生しました。"

            TablePrinter(context).execute()

            expected = u'''\
予期せぬ例外が発生しました。
'''
            actual = stdout.getvalue().decode("utf-8")
            self.assertEqual(expected, actual)

    def test__display_of(self):
        # type: () -> None

        # ---- パターン1 ----
        context = self._default_context()
        expected = u"\u005c"
        actual = TablePrinter(context)._display_of(u"\\")
        self.assertEqual(expected, actual)

        # ---- パターン2 ----
        context = self._default_context()
        expected = r"a\nb\nc\nd\ne"
        actual = TablePrinter(context)._display_of(u"a\nb\nc\nd\ne")
        self.assertEqual(expected, actual)

        # ---- パターン3 ----
        context = self._default_context()
        expected = r"abcde"
        actual = TablePrinter(context)._display_of(u"\nabcde\n")
        self.assertEqual(expected, actual)

        # ---- パターン4 ----
        context = self._default_context()
        context.column_max_length = 3
        expected = r"abc"
        actual = TablePrinter(context)._display_of(u"abc")
        self.assertEqual(expected, actual)

        # ---- パターン5 ----
        context = self._default_context()
        context.column_max_length = 3
        expected = r"a...d"
        actual = TablePrinter(context)._display_of(u"abcd")
        self.assertEqual(expected, actual)

        # ---- パターン6 ----
        context = self._default_context()
        context.column_max_length = 3
        expected = r"a...e"
        actual = TablePrinter(context)._display_of(u"abcde")
        self.assertEqual(expected, actual)

        # ---- パターン7 ----
        context = self._default_context()
        context.column_max_length = 3
        expected = r"a...f"
        actual = TablePrinter(context)._display_of(u"abcdef")
        self.assertEqual(expected, actual)

        # ---- パターン8 ----
        context = self._default_context()
        context.column_max_length = 3
        expected = r"a...g"
        actual = TablePrinter(context)._display_of(u"abcdefg")
        self.assertEqual(expected, actual)

        # ---- パターン9 ----
        context = self._default_context()
        context.column_max_length = 5
        expected = r"ab...mn"
        actual = TablePrinter(context)._display_of(u"abcdefghijklmn")
        self.assertEqual(expected, actual)

        # ---- パターン10 ----
        context = self._default_context()
        context.column_max_length = 5
        expected = u"あい...せそ"
        actual = TablePrinter(context)._display_of(u"あいうえおかきくけこさしすせそ")
        self.assertEqual(expected, actual)

        # ---- パターン11 ----
        context = self._default_context()
        context.column_max_length = 5
        expected = u"𠀋...𣗄"
        actual = TablePrinter(context)._display_of(u'𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄')
        self.assertEqual(expected, actual)

    def test__length_of(self):
        # type: () -> None

        context = mock.MagicMock()

        # ---- パターン1 ----
        expected = 1
        actual = TablePrinter(context)._length_of(u"\\")
        self.assertEqual(expected, actual)

        # ---- パターン2 ----
        expected = 1
        actual = TablePrinter(context)._length_of(u"\u005c")  # \u005c = \
        self.assertEqual(expected, actual)

        # ---- パターン3 ----
        expected = 2
        actual = TablePrinter(context)._length_of(u"あ")
        self.assertEqual(expected, actual)

        # ---- パターン4 ----
        expected = 11
        actual = TablePrinter(context)._length_of(u'," ./\\=?!:;')
        self.assertEqual(expected, actual)

        # ---- パターン5 ----
        expected = 16
        actual = TablePrinter(context)._length_of(u'ヲンヰヱヴーヾ・')
        self.assertEqual(expected, actual)

        # ---- パターン6 ----
        expected = 7
        actual = TablePrinter(context)._length_of(u'ｧｰｭｿﾏﾞﾟ')
        self.assertEqual(expected, actual)

        # ---- パターン7 ----
        expected = 16
        actual = TablePrinter(context)._length_of(u'㌶Ⅲ⑳㏾☎㈱髙﨑')
        self.assertEqual(expected, actual)

        # ---- パターン8 ----
        expected = 10
        actual = TablePrinter(context)._length_of(u'¢£¬‖−〜―')
        self.assertEqual(expected, actual)

        # ---- パターン9 ----
        expected = 20
        actual = TablePrinter(context)._length_of(u'𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄')
        self.assertEqual(expected, actual)

        # ---- パターン10 ----
        expected = 6
        actual = TablePrinter(context)._length_of(u'ソ能表')
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.column_max_length = 500
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
