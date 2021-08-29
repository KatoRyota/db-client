# coding: utf-8
import HTMLParser
import logging
from logging import Logger

from ..context.context import Context


class MysqlParser(HTMLParser.HTMLParser, object):
    __slots__ = (
        "__logger",
        "__context",
        "__is_processing_body",
        "__is_processing_table",
        "__is_processing_heading",
        "__is_processing_data",
        "__processing_record",
        "__processing_heading",
        "__processing_data",
        "__row_count"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(MysqlParser, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context
        self.__is_processing_body = False  # type: bool
        self.__is_processing_table = False  # type: bool
        self.__is_processing_heading = False  # type: bool
        self.__is_processing_data = False  # type: bool
        self.__processing_record = []  # type: list
        self.__processing_heading = u""  # type: unicode
        self.__processing_data = u""  # type: unicode
        self.__row_count = 0  # type: int

    def execute(self):
        # type: () -> None

        context = self.__context
        self.feed(context.result_set_html)

        if not context.result_sets and not context.result_headings and not context.result_message:
            context.result_message = context.result_set_html

        self.close()

    def handle_starttag(self, tag, attrs):
        # type: (unicode, list) -> None

        if tag == "body":
            self.__is_processing_body = True
        if tag == "table":
            self.__is_processing_table = True
        if tag == "tr":
            self.__row_count += 1
        if tag == "th":
            self.__is_processing_heading = True
        if tag == "td":
            self.__is_processing_data = True

    def handle_endtag(self, tag):
        # type: (unicode) -> None

        context = self.__context

        if tag == "body":
            self.__is_processing_body = False
        if tag == "table":
            self.__is_processing_table = False
        if tag == "tr":
            if self.__processing_record:
                context.result_sets.append(self.__processing_record)
            self.__processing_record = []
        if tag == "th":
            self.__is_processing_heading = False
            if self.__row_count == 1:
                context.result_headings.append(self.__processing_heading)
            self.__processing_heading = u""
        if tag == "td":
            self.__is_processing_data = False
            self.__processing_record.append(self.__processing_data)
            self.__processing_data = u""

    def handle_data(self, data):
        # type: (unicode) -> None

        context = self.__context

        if self.__is_processing_heading:
            self.__processing_heading += data
        elif self.__is_processing_data:
            self.__processing_data += data
        elif self.__is_processing_body and not self.__is_processing_table:
            context.result_message += data

    def handle_entityref(self, name):
        # type: (unicode) -> None

        context = self.__context

        if self.__is_processing_heading:
            self.__processing_heading += self.unescape("&%s;" % name)
        elif self.__is_processing_data:
            self.__processing_data += self.unescape("&%s;" % name)
        elif self.__is_processing_body and not self.__is_processing_table:
            context.result_message += self.unescape("&%s;" % name)

    def handle_charref(self, name):
        # type: (unicode) -> None

        context = self.__context

        if self.__is_processing_heading:
            self.__processing_heading += self.unescape("&#%s;" % name)
        elif self.__is_processing_data:
            self.__processing_data += self.unescape("&#%s;" % name)
        elif self.__is_processing_body and not self.__is_processing_table:
            context.result_message += self.unescape("&#%s;" % name)
