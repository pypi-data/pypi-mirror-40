import logging
import sys
import json
import traceback
from .log_filters import AddContextualFieldFilter, MaskPasswordsInLogs


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        json_dict = {}

        if record.exc_info:
            json_dict['stack_trace'] = _sanitize_stacktrace_for_json_fields(*record.exc_info)

            # mark exception info as none to consume the exception here and stop propogation
            # where it might get logged to sys.stderr.
            # If we need to reraise it we can log it as an exception on the root logger
            record.exc_info = None

        json_dict.update(record.__dict__)

        # Already replaced this with 'stack_trace', no longer needed
        assert json_dict['exc_info'] is None
        del json_dict['exc_info']

        # We don't need these 2 fields as message field has msg % args now
        json_dict['message'] = record.getMessage()
        del json_dict['msg']
        del json_dict['args']

        json_dict['level'] = json_dict['levelname']
        del json_dict['levelname']

        try:
            return json.dumps(json_dict)
        except (TypeError, OverflowError):
            return json.dumps({
                "message":
                "An unrecoverable exception occured while logging"
            })


def _sanitize_stacktrace_for_json_fields(type, value, traceback) -> str:
    lines = traceback.format_exception(type, value, traceback)
    return "".join(lines)


def _uncaught_exception_logger(
    exception_type: BaseException,
    exception_value: Exception,
    exception_traceback: traceback.TracebackException
):
    exception_traceback_string = _sanitize_stacktrace_for_json_fields(
        exception_type,
        exception_value,
        exception_traceback,
    )
    # raise to root logger where it will be consumed by the formatter attached to our handler
    logging.getLogger().error(exception_traceback_string)


_default_formatter = logging.Formatter(
        '[%(levelname)s -- %(asctime)s] :: (%(module)s.%(funcName)s) :: %(message)s',
        "%H:%M:%S"
    )


def configure_logging(_logger_name: str, level: str, log_format: str = 'json') -> logging.Logger:
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(level)

    assert logger.hasHandlers()
    for handler in logger.handlers:
        if log_format != 'console':
            handler.setFormatter(JSONFormatter())
        else:
            handler.setFormatter(_default_formatter)
        handler.addFilter(MaskPasswordsInLogs())
        handler.addFilter(AddContextualFieldFilter('service', 'rms'))

    sys.excepthook = _uncaught_exception_logger

    return logging.getLogger(_logger_name)
