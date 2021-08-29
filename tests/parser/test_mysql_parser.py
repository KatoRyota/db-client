# coding: utf-8
import unittest
from unittest import TestCase

from dbclient.context.context import Context
from dbclient.parser.mysql_parser import MysqlParser


class TestMysqlParser(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        # 前提条件
        context = self._default_context()

        # 実行
        MysqlParser(context).execute()

        # 検証
        actual = len(context.result_headings)
        expected = 3
        self.assertEqual(expected, actual)

        actual = context.result_headings[0]
        expected = u"id"
        self.assertEqual(expected, actual)

        actual = context.result_headings[1]
        expected = u"name"
        self.assertEqual(expected, actual)

        actual = context.result_headings[2]
        expected = u"type"
        self.assertEqual(expected, actual)

        actual = len(context.result_sets)
        expected = 2
        self.assertEqual(expected, actual)

        actual = len(context.result_sets[1])
        expected = 3
        self.assertEqual(expected, actual)

        actual = context.result_sets[1][0]
        expected = u'あ\nいうえお'
        self.assertEqual(expected, actual)

        actual = context.result_sets[1][1]
        expected = u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表'
        self.assertEqual(expected, actual)

        actual = context.result_sets[1][2]
        expected = u'<<<©©©&&&'
        self.assertEqual(expected, actual)

        actual = context.result_message.strip()
        expected = u''
        self.assertEqual(expected, actual)

        # ---- ケース2 ----
        # 前提条件
        context = self._default_context()
        context.result_set_html = u"エラーが発生しました。"

        # 実行
        MysqlParser(context).execute()

        # 検証
        actual = len(context.result_headings)
        expected = 0
        self.assertEqual(expected, actual)

        actual = len(context.result_sets)
        expected = 0
        self.assertEqual(expected, actual)

        actual = context.result_message.strip()
        expected = u"エラーが発生しました。"
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.result_set_html = u'''\
<TABLE BORDER=1>
    <TR>
        <TH>id</TH>
        <TH>name</TH>
        <TH>type</TH>
    </TR>
    <TR>
        <TD>ID-000-0000</TD>
        <TD>NAME-000-0000</TD>
        <TD>TYPE-000-0000</TD>
    </TR>
    <TR>
        <TD>あ\nいうえお</TD>
        <TD>," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表</TD>
        <TD>&lt;&#60;&#x3c;&copy;&#169;&#xa9;&amp;&#38;&#x26;</TD>
    </TR>
</TABLE>
'''
        return context


if __name__ == "__main__":
    unittest.main()
