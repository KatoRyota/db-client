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

        if not self.__context.sql_client_return_code == 0:
            print self.__context.result_message.strip().encode("utf-8")
            return

        # ---- CSV形式で標準出力に出力 ----
        for index, record in enumerate(self.__context.result_sets):  # type: (int, list)

            if index == 0:
                if self.__context.heading == Context.Heading.ON and self.__context.result_headings:
                    self._print_csv_row(self.__context.result_headings)

            if index != 0 and \
                    self.__context.pagesize != 0 and \
                    index % self.__context.pagesize == 0:

                print

                if self.__context.heading == Context.Heading.ON and self.__context.result_headings:
                    self._print_csv_row(self.__context.result_headings)

            self._print_csv_row(record)

        if self.__context.feedback == Context.Feedback.ON and self.__context.result_message:
            print
            print "---- Result Message ----"
            print self.__context.result_message.strip().encode("utf-8")

    def _print_csv_row(self, record):
        # type: (list) -> None

        row = u""

        for index, column in enumerate(record):  # type: (int, unicode)
            display_column = column.strip()
            display_column = re.sub(r"\\".decode("utf-8"), r"\\\\".decode("utf-8"), display_column)
            display_column = re.sub(r"\n".decode("utf-8"), r"\\n".decode("utf-8"), display_column)

            if index + 1 < len(record):
                row += display_column + self.__context.field_delimiter
            elif index + 1 == len(record):
                row += display_column

        if row:
            print row.encode("utf-8")
