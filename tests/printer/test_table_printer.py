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
        context = Context()
        context.column_max_length = 100
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
        context.result_message = u"4件のレコードが選択されました。"

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

---- Result Message ----
4件のレコードが選択されました。
'''

        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            TablePrinter(context).execute()
            self.assertEqual(expected, stdout.getvalue().decode("utf-8"))

        # ---- パターン2 ----
        context = Context()
        context.column_max_length = 1000
        context.heading = "on"
        context.feedback = "on"
        context.pagesize = 3
        context.sql_client_return_code = 0
        context.result_headings = ["ID", "NAME", "TYPE"]
        context.result_sets = []
        context.result_sets.append([
            u'あ\nいうえお',
            u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表',
            u'<input type="text" value="<font color="red">&lt;&copy;&amp;'])

        context.result_message = \
            u'あ\nいうえお' \
            u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表' \
            u'<input type="text" value="<font color="red">&lt;&copy;&amp;'

        expected = u'''\
+------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------+
|ID          |NAME                                                                                                      |TYPE                                                       |
+------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------+
|あ\\nいうえお|," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表|<input type="text" value="<font color="red">&lt;&copy;&amp;|
+------------+----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------+

---- Result Message ----
あ
いうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表<input type="text" value="<font color="red">&lt;&copy;&amp;
'''

        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            TablePrinter(context).execute()
            self.assertEqual(expected, stdout.getvalue().decode("utf-8"))

    def test__length_of(self):
        # type: () -> None

        # ---- パターン1 ----
        context = mock.MagicMock()

        expected = 1

        with mock.patch("sys.stdout", new=StringIO()) as stdout:  # type: StringIO
            length = TablePrinter(context)._length_of(u'\\')
            self.assertEqual(expected, length)


if __name__ == "__main__":
    unittest.main()
