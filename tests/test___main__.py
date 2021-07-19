# coding: utf-8
import unittest
from unittest import TestCase

import mock


class TestMain(TestCase):

    def test_main(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdout"), \
                mock.patch("sys.stderr"), \
                mock.patch("os.makedirs"), \
                mock.patch("dbclient.runner.oracle_runner.OracleRunner.execute") as oracle_runner_execute:
            from dbclient import __main__

        expected = "table"
        actual = __main__.context.display_format
        self.assertEqual(expected, actual)

        expected = ""
        actual = __main__.context.field_delimiter
        self.assertEqual(expected, actual)

        expected = 1000
        actual = __main__.context.column_max_length
        self.assertEqual(expected, actual)

        expected = "on"
        actual = __main__.context.heading
        self.assertEqual(expected, actual)

        expected = "on"
        actual = __main__.context.feedback
        self.assertEqual(expected, actual)

        expected = 10
        actual = __main__.context.pagesize
        self.assertEqual(expected, actual)

        expected = "default"
        actual = __main__.context.connection_target
        self.assertEqual(expected, actual)

        oracle_runner_execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
