# coding: utf-8
import platform
import unittest
from io import BytesIO
from unittest import TestCase

import mock

from dbclient.context.context import Context
from dbclient.printer.table_printer import TablePrinter


class TestTablePrinter(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
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
            self.assertEqual(expected, actual)

        # ---- ケース2 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
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

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
+------------+---------------------------------------------------------------------------------------+-----------------------------------------------------------+
|ID          |NAME                                                                                   |TYPE                                                       |
+------------+---------------------------------------------------------------------------------------+-----------------------------------------------------------+
|あ\\nいうえお|," ./\\\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表|<input type="text" value="<font color="red">&lt;&copy;&amp;|
+------------+---------------------------------------------------------------------------------------+-----------------------------------------------------------+

あ
いうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表<input type="text" value="<font color="red">&lt;&copy;&amp;
'''
            self.assertEqual(expected, actual)

        # ---- ケース3 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            context.result_headings = []
            context.result_sets = []

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
4行が選択されました。
'''
            self.assertEqual(expected, actual)

        # ---- ケース4 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            context.result_message = u''

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
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
            self.assertEqual(expected, actual)

        # ---- ケース5 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            context.heading = "off"

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
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
            self.assertEqual(expected, actual)

        # ---- ケース6 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            context.feedback = "off"

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
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
            self.assertEqual(expected, actual)

        # ---- ケース7 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = self._default_context()

            context.sql_client_return_code = 1
            context.result_message = u"予期せぬ例外が発生しました。"

            # 実行
            TablePrinter(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
予期せぬ例外が発生しました。
'''
            self.assertEqual(expected, actual)

    def test__display_of(self):
        # type: () -> None

        # ---- ケース1 ----
        context = self._default_context()
        actual = TablePrinter(context)._display_of(u"\\")
        expected = u"\u005c\u005c"
        self.assertEqual(expected, actual)

        # ---- ケース2 ----
        context = self._default_context()
        actual = TablePrinter(context)._display_of(u"a\nb\nc\nd\ne")
        expected = r"a\nb\nc\nd\ne"
        self.assertEqual(expected, actual)

        # ---- ケース3 ----
        context = self._default_context()
        actual = TablePrinter(context)._display_of(u"\nabcde\n")
        expected = r"abcde"
        self.assertEqual(expected, actual)

        # ---- ケース4 ----
        context = self._default_context()
        context.column_max_length = 3
        actual = TablePrinter(context)._display_of(u"abc")
        expected = r"abc"
        self.assertEqual(expected, actual)

        # ---- ケース5 ----
        context = self._default_context()
        context.column_max_length = 3
        actual = TablePrinter(context)._display_of(u"abcd")
        expected = r"a...d"
        self.assertEqual(expected, actual)

        # ---- ケース6 ----
        context = self._default_context()
        context.column_max_length = 3
        actual = TablePrinter(context)._display_of(u"abcde")
        expected = r"a...e"
        self.assertEqual(expected, actual)

        # ---- ケース7 ----
        context = self._default_context()
        context.column_max_length = 3
        actual = TablePrinter(context)._display_of(u"abcdef")
        expected = r"a...f"
        self.assertEqual(expected, actual)

        # ---- ケース8 ----
        context = self._default_context()
        context.column_max_length = 3
        actual = TablePrinter(context)._display_of(u"abcdefg")
        expected = r"a...g"
        self.assertEqual(expected, actual)

        # ---- ケース9 ----
        context = self._default_context()
        context.column_max_length = 5
        actual = TablePrinter(context)._display_of(u"abcdefghijklmn")
        expected = r"ab...mn"
        self.assertEqual(expected, actual)

        # ---- ケース10 ----
        context = self._default_context()
        context.column_max_length = 5
        actual = TablePrinter(context)._display_of(u"あいうえおかきくけこさしすせそ")
        expected = u"あい...せそ"
        self.assertEqual(expected, actual)

        # ---- ケース11 ----
        if platform.system() == "Windows":
            context = self._default_context()
            context.column_max_length = 5
            actual = TablePrinter(context)._display_of(u'𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄')
            expected = u"𠀋...𣗄"
            self.assertEqual(expected, actual)
        else:
            context = self._default_context()
            context.column_max_length = 5
            actual = TablePrinter(context)._display_of(u'𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄')
            expected = u"𠀋𡈽...𣇄𣗄"
            self.assertEqual(expected, actual)

    def test__length_of(self):
        # type: () -> None

        context = mock.MagicMock()

        # ---- ケース1 ----
        actual = TablePrinter(context)._length_of(u'," ./\\=?!:;')
        expected = 11
        self.assertEqual(expected, actual)

        # ---- ケース2 ----
        actual = TablePrinter(context)._length_of(u'ヲンヰヱヴーヾ・')
        expected = 16
        self.assertEqual(expected, actual)

        # ---- ケース3 ----
        actual = TablePrinter(context)._length_of(u'ｧｰｭｿﾏﾞﾟ')
        expected = 7
        self.assertEqual(expected, actual)

        # ---- ケース4 ----
        actual = TablePrinter(context)._length_of(u'㌶Ⅲ⑳㏾☎㈱髙﨑')
        expected = 16
        self.assertEqual(expected, actual)

        # ---- ケース5 ----
        actual = TablePrinter(context)._length_of(u'¢£¬‖−〜―')
        expected = 10
        self.assertEqual(expected, actual)

        # ---- ケース6 ----
        actual = TablePrinter(context)._length_of(u'𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄')
        expected = 20
        self.assertEqual(expected, actual)

        # ---- ケース7 ----
        actual = TablePrinter(context)._length_of(u'ソ能表')
        expected = 6
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
