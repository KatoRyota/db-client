# coding: utf-8

import unittest
from unittest import TestCase

from dbclient.context.context import Context
from dbclient.parser.oracle_parser import OracleParser


class TestOracleParser(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- パターン1 ----
        context = self._default_context()
        OracleParser(context).execute()

        expected = u"ID"
        actual = context.result_headings[0]
        self.assertEqual(expected, actual)

        expected = u"NAME"
        actual = context.result_headings[1]
        self.assertEqual(expected, actual)

        expected = u"TYPE"
        actual = context.result_headings[2]
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
            <td>ID-111-1111</td>
            <td>NAME-111-1111</td>
            <td>TYPE-111-1111</td>
        </tr>
    </table>
    <p>2行が選択されました。<br><br>
</body>
</html>
'''
        return context


if __name__ == "__main__":
    unittest.main()
