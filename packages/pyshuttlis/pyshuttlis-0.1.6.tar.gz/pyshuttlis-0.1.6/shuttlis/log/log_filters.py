import logging


class AddContextualFieldFilter(logging.Filter):
    def __init__(self, field_name: str, field_value: str) -> None:
        self._field_name: str = field_name
        self._field_value: str = field_value

    # SerivceLogRecord: Union[logging.LogRecord, str]
    def filter(self, record: logging.LogRecord) -> bool:
        record.__dict__[self._field_name] = self._field_value
        return True


class MaskPasswordsInLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.__dict__.get('password', None) is not None:
            record.__dict__['password'] = "******"
        return True
