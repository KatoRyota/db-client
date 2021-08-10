# coding: utf-8
import unittest
from unittest import TestCase

from dbclient.context.context import Context
from dbclient.parser.oracle_parser import OracleParser


class TestOracleParser(TestCase):

    def test_execute(self):
        # type: () -> None

        context = self._default_context()
        OracleParser(context).execute()

        actual = len(context.result_headings)
        expected = 3
        self.assertEqual(expected, actual)

        actual = context.result_headings[0]
        expected = u"ID"
        self.assertEqual(expected, actual)

        actual = context.result_headings[1]
        expected = u"NAME"
        self.assertEqual(expected, actual)

        actual = context.result_headings[2]
        expected = u"TYPE"
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
        expected = u'あ\nいうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表<<<©©©&&&'
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.result_set_html = u'''\
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="generator" content="SQL*Plus 19.11.0">
    <style type='text/css'>
        body {
            font: 10pt Arial, Helvetica, sans-serif;
            color: black;
            background: White;
        }

        p {
            font: 10pt Arial, Helvetica, sans-serif;
            color: black;
            background: White;
        }

        table,
        tr,
        td {
            font: 10pt Arial, Helvetica, sans-serif;
            color: Black;
            background: #f7f7e7;
            padding: 0px 0px 0px 0px;
            margin: 0px 0px 0px 0px;
        }

        th {
            font: bold 10pt Arial, Helvetica, sans-serif;
            color: #336699;
            background: #cccc99;
            padding: 0px 0px 0px 0px;
        }

        h1 {
            font: 16pt Arial, Helvetica, Geneva, sans-serif;
            color: #336699;
            background-color: White;
            border-bottom: 1px solid #cccc99;
            margin-top: 0pt;
            margin-bottom: 0pt;
            padding: 0px 0px 0px 0px;
            -
        }

        h2 {
            font: bold 10pt Arial, Helvetica, Geneva, sans-serif;
            color: #336699;
            background-color: White;
            margin-top: 4pt;
            margin-bottom: 0pt;
        }

        a {
            font: 9pt Arial, Helvetica, sans-serif;
            color: #663300;
            background: #ffffff;
            margin-top: 0pt;
            margin-bottom: 0pt;
            vertical-align: top;
        }
    </style>
    <title>SQL*Plus Report</title>
</head>

<body>
    <p>
    <table border='1' width='90%' align='center' summary='Script output'>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">NAME</th>
            <th scope="col">TYPE</th>
        </tr>
        <tr>
            <td>ID-000-0000</td>
            <td>NAME-000-0000</td>
            <td>TYPE-000-0000</td>
        </tr>
        <tr>
            <td>あ\nいうえお</td>
            <td>," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表</td>
            <td>&lt;&#60;&#x3c;&copy;&#169;&#xa9;&amp;&#38;&#x26;</td>
        </tr>
    </table>
    <p>あ\nいうえお," ./\\=?!:;ヲンヰヱヴーヾ・ｧｰｭｿﾏﾞﾟ㌶Ⅲ⑳㏾☎㈱髙﨑¢£¬‖−〜―𠀋𡈽𡌛𡑮𡢽𠮟𡚴𡸴𣇄𣗄ソ能表&lt;&#60;&#x3c;&copy;&#169;&#xa9;&amp;&#38;&#x26;<br><br>
</body>

</html>
'''
        return context


if __name__ == "__main__":
    unittest.main()
