# coding: utf-8
import logging
import os
from ConfigParser import SafeConfigParser
from logging import Logger


class Context(object):
    __slots__ = (
        "__logger",
        "config",
        "root_dir",
        "profile",
        "config_dir",
        "log_dir",
        "subprocesses",
        "display_format",
        "field_delimiter",
        "column_max_length",
        "heading",
        "feedback",
        "pagesize",
        "connection_target",
        "sql",
        "dsn",
        "sql_client_return_code",
        "result_set_html",
        "result_headings",
        "result_sets",
        "result_message"
    )

    def __init__(self):
        # type: () -> None

        super(Context, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.config = SafeConfigParser()  # type: SafeConfigParser
        self.root_dir = ""  # type: str
        self.profile = ""  # type: str
        self.config_dir = ""  # type: str
        self.log_dir = ""  # type: str
        self.subprocesses = []  # type: list
        self.display_format = ""  # type: str
        self.field_delimiter = ""  # type: str
        self.column_max_length = 0  # type: int
        self.heading = ""  # type: str
        self.feedback = ""  # type: str
        self.pagesize = 0  # type: int
        self.sql = u""  # type: unicode
        self.dsn = ""  # type: str
        self.connection_target = ""  # type: str
        self.sql_client_return_code = 0  # type: int
        self.result_set_html = u""  # type: unicode
        self.result_headings = []  # type: list
        self.result_sets = []  # type: list
        self.result_message = u""  # type: unicode

    def check_application_initialize(self):
        # type: () -> bool

        if not isinstance(self.config, SafeConfigParser):
            return False

        if not self.root_dir:
            return False
        if type(self.root_dir) is not str:
            return False
        if not os.path.isdir(self.root_dir):
            return False

        if not self.profile:
            return False
        if type(self.profile) is not str:
            return False

        if not self.config_dir:
            return False
        if type(self.config_dir) is not str:
            return False
        if not os.path.isdir(self.config_dir):
            return False

        if not self.log_dir:
            return False
        if type(self.log_dir) is not str:
            return False
        if not os.path.isdir(self.log_dir):
            return False

        return True

    def check_option_parse(self):
        # type: () -> bool

        if not (self.display_format == Context.DisplayFormat.TABLE or
                self.display_format == Context.DisplayFormat.CSV):
            return False

        if self.display_format == Context.DisplayFormat.CSV:
            if not self.field_delimiter:
                return False
            if type(self.field_delimiter) is not str:
                return False

        if self.display_format == Context.DisplayFormat.TABLE:
            if type(self.column_max_length) is not int:
                return False
            if self.column_max_length < 1:
                return False

        if not (self.heading == Context.Heading.ON or
                self.heading == Context.Heading.OFF):
            return False

        if not (self.feedback == Context.Feedback.ON or
                self.feedback == Context.Feedback.OFF):
            return False

        if type(self.pagesize) is not int:
            return False
        if self.pagesize < 0:
            return False

        if not self.connection_target:
            return False
        if type(self.connection_target) is not str:
            return False

        return True

    def check_sql_execute(self):
        # type: () -> bool

        if type(self.subprocesses) is not list:
            return False

        if not self.sql:
            return False
        if type(self.sql) is not unicode:
            return False

        if not self.dsn:
            return False
        if type(self.dsn) is not str:
            return False

        if type(self.sql_client_return_code) is not int:
            return False

        if type(self.result_set_html) is not unicode:
            return False

        return True

    def check_result_set_parse(self):
        # type: () -> bool

        if type(self.result_headings) is not list:
            return False

        if type(self.result_sets) is not list:
            return False

        if type(self.result_message) is not unicode:
            return False

        return True

    class DisplayFormat(object):
        TABLE = "table"  # type: str
        CSV = "csv"  # type: str

    class Heading(object):
        ON = "on"  # type: str
        OFF = "off"  # type: str

    class Feedback(object):
        ON = "on"  # type: str
        OFF = "off"  # type: str

    class DataBase(object):
        ORACLE = "oracle"  # type: str
        MYSQL = "mysql"  # type: str
