# coding: utf-8

import unittest
from unittest import TestCase

from dbclient.context.context import Context
from dbclient.parser.mysql_parser import MysqlParser


class TestMysqlParser(TestCase):

    def test_execute(self):
        # type: () -> None

        context = self._default_context()
        MysqlParser(context).execute()

        expected = 3
        actual = len(context.result_headings)
        self.assertEqual(expected, actual)

        expected = u"id"
        actual = context.result_headings[0]
        self.assertEqual(expected, actual)

        expected = u"name"
        actual = context.result_headings[1]
        self.assertEqual(expected, actual)

        expected = u"type"
        actual = context.result_headings[2]
        self.assertEqual(expected, actual)

        expected = 2
        actual = len(context.result_sets)
        self.assertEqual(expected, actual)

        expected = 3
        actual = len(context.result_sets[1])
        self.assertEqual(expected, actual)

        expected = u'あ\nいうえお'
        actual = context.result_sets[1][0]
        self.assertEqual(expected, actual)

        expected = u'," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表'
        actual = context.result_sets[1][1]
        self.assertEqual(expected, actual)

        expected = u'<<<©©©&&&'
        actual = context.result_sets[1][2]
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
