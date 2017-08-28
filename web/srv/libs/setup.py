import logging
from logging import StreamHandler
import socket
import sys


def log(name: str, version: str, **options):
    """
    log configuration setup, logging all goes to standard out by default
    :param str name: endpoint name
    :param str version: endpoint version
    :param options: TODO other options for other chat notifications (sms,
    :return:
    """
    # DO NOT 'log' anything here, logging is being set up so infinite loops happen
    print(f'entered log({locals()})')
    log_format = '{asctime} [{app_host} | {app_name} | {app_vers} | {process}] [{levelname}] {filename}:{lineno} - {message}'

    try:
        host = socket.gethostname()
    except:
        host = "?"

    def filter_factory():
        class LoggingFilter(logging.Filter):
            def filter(self, record):
                try:
                    record.app_host = host
                except:
                    record.app_host = '?host?'

                try:
                    record.app_name = name
                except:
                    record.app_name = '?name?'

                try:
                    record.app_vers = version
                except:
                    record.app_vers = '?vers?'

                return True
        return LoggingFilter

    formatter = logging.Formatter(log_format, style="{")
    LogFilter = filter_factory()
    new_logger = logging.root
    new_logger.setLevel(logging.DEBUG)

    # standard out
    log_handler_s = StreamHandler(sys.stdout)
    log_handler_s.setLevel(logging.DEBUG)
    log_handler_s.setFormatter(formatter)
    log_handler_s.addFilter(LogFilter())
    new_logger.addHandler(log_handler_s)

    return new_logger
