# coding: utf-8
import logging
import math
import re
from logging import Logger

from ..context.context import Context


class TablePrinter(object):
    __slots__ = (
        "__logger",
        "__context",
        "__column_width_list"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(TablePrinter, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context
        self.__column_width_list = []  # type: list

    def execute(self):
        # type: () -> None

        if not self.__context.sql_client_return_code == 0:
            print self.__context.result_message.strip().encode("utf-8")
            return

        # ---- カラム幅を計算 ----
        if self.__context.result_sets:
            self.__column_width_list = [0 for _ in range(len(self.__context.result_sets[0]))]

        for record in self.__context.result_sets:  # type: list
            for index, column in enumerate(record):  # type: (int, unicode)
                display_column = self._display_of(column)
                display_column_length = self._length_of(display_column)

                if self.__column_width_list[index] < display_column_length:
                    self.__column_width_list[index] = display_column_length

        if self.__context.heading == Context.Heading.ON and self.__context.result_headings:
            for index, column in enumerate(self.__context.result_headings):  # type: (int, unicode)
                display_column = self._display_of(column)
                display_column_length = self._length_of(display_column)

                if self.__column_width_list[index] < display_column_length:
                    self.__column_width_list[index] = display_column_length

        # ---- テーブル形式で標準出力に出力 ----
        for index, record in enumerate(self.__context.result_sets):  # type: (int, list)

            if index == 0:
                if self.__context.heading == Context.Heading.ON and self.__context.result_headings:
                    self._print_table_border()
                    self._print_table_row(self.__context.result_headings)
                    self._print_table_border()
                else:
                    self._print_table_border()

            if index != 0 and \
                    self.__context.pagesize != 0 and \
                    index % self.__context.pagesize == 0:

                print

                if self.__context.heading == Context.Heading.ON and self.__context.result_headings:
                    self._print_table_border()
                    self._print_table_row(self.__context.result_headings)
                    self._print_table_border()
                else:
                    self._print_table_border()

            self._print_table_row(record)
            self._print_table_border()

        if self.__context.feedback == Context.Feedback.ON and self.__context.result_message:
            print
            print self.__context.result_message.strip().encode("utf-8")

    def _print_table_row(self, record):
        # type: (list) -> None

        row = u""

        for index, column in enumerate(record):  # type: (int, unicode)

            if index == 0:
                row = u"|"

            display_column = self._display_of(column)
            display_column_length = self._length_of(display_column)
            space = u" " * (self.__column_width_list[index] - display_column_length)
            row += display_column + space + u"|"

        if row:
            print row.encode("utf-8")

    def _print_table_border(self):
        # type: () -> None

        border = u""

        for index, column_width in enumerate(self.__column_width_list):  # type: int

            if index == 0:
                border = u"+"

            border += u"-" * column_width + u"+"

        if border:
            print border.encode("utf-8")

    def _display_of(self, column):
        # type: (unicode) -> unicode

        display_column = column.strip()
        # TODO: 下記をコメントを外してしてテストする
        # display_column = re.sub(u'\\\\', u"\\\\\\\\", display_column)
        display_column = re.sub(u"\n", u"\\\\n", display_column)
        display_column_length = self._length_of(display_column)

        if self.__context.column_max_length < 1 or display_column_length <= self.__context.column_max_length:
            return display_column

        elif display_column_length > self.__context.column_max_length:
            half_length = math.floor(self.__context.column_max_length / 2)
            half_length = int(half_length)
            pattern = r"^(.{%s}).*(.{%s})$".decode("utf-8") % (half_length, half_length)
            display_column = re.sub(pattern, r"\1...\2".decode("utf-8"), display_column)
            return display_column

    @staticmethod
    def _length_of(chars):
        # type: (unicode) -> int

        # 下記で指定してる、Unicodeのコードポイントは、以下を参考にした。
        #   * https://ja.wikipedia.org/wiki/Unicode%E4%B8%80%E8%A6%A7_0000-0FFF
        #   * https://ja.wikipedia.org/wiki/Unicode%E4%B8%80%E8%A6%A7_F000-FFFF

        chars = re.sub(u"𠀋|𡈽|𡌛|𡑮|𡢽|𠮟|𡚴|𡸴|𣇄|𣗄", u"？", chars)

        character_length = 0

        for char in chars:  # type: unicode
            if re.match(u"[\u00a2\u00a3\u00ac\u2212]", char):
                character_length += 1
                continue

            if re.match(u"[\u0020-\u007E\uFF61-\uFF9F]", char):
                character_length += 1
            else:
                character_length += 2

        return character_length
