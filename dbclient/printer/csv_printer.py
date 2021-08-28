# coding: utf-8
import logging
import re
from logging import Logger

from ..context.context import Context


class CsvPrinter(object):
    __slots__ = (
        "__logger",
        "__context"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(CsvPrinter, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context

    def execute(self):
        # type: () -> None

        context = self.__context

        if not context.sql_client_return_code == 0:
            if context.result_message.strip():
                print context.result_message.strip().encode("utf-8")

            return

        if not context.result_sets:
            if context.result_message.strip():
                print context.result_message.strip().encode("utf-8")

            return

        # ---- CSV形式で標準出力に出力 ----
        for index, record in enumerate(context.result_sets):  # type: (int, list)

            if index == 0:
                if context.heading == Context.Heading.ON and context.result_headings:
                    self._print_csv_row(context.result_headings)

            if index != 0 and \
                    context.pagesize != 0 and \
                    index % context.pagesize == 0:

                print

                if context.heading == Context.Heading.ON and context.result_headings:
                    self._print_csv_row(context.result_headings)

            self._print_csv_row(record)

        if context.feedback == Context.Feedback.ON and context.result_message.strip():
            print
            print context.result_message.strip().encode("utf-8")

    def _print_csv_row(self, record):
        # type: (list) -> None

        context = self.__context
        row = u""

        for index, column in enumerate(record):  # type: (int, unicode)
            display_column = column.strip()
            display_column = re.sub(u'\\\\', u"\\\\\\\\", display_column)
            display_column = re.sub(u"\r", u"\\\\r", display_column)
            display_column = re.sub(u"\n", u"\\\\n", display_column)

            if index + 1 < len(record):
                row += display_column + context.field_delimiter
            elif index + 1 == len(record):
                row += display_column

        if row:
            print row.encode("utf-8")
