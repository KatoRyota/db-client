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

        expected = u""
        actual = u""
        self.assertEqual(expected, actual)

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.result_set_html = u'''\
'''
        return context


if __name__ == "__main__":
    unittest.main()
