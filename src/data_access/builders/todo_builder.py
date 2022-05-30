from src.common.get_config import get_config
from src.data_access.models.todo_entry import TodoEntry

from datetime import datetime as dt

from src.middleware.exc.todos import *


class TodoBuilder:
    _datetime = None

    def __init__(self, user_id: int, title: str):
        self._user_id = user_id
        self._title = title

    def set_date_time(self, date_time: str):
        datetime_format = None
        try:
            datetime_format = get_config()["DATETIME_FORMAT"]
            date_time_parsed = dt.strptime(date_time, datetime_format)
            self._date_time = date_time_parsed
            return self
        except KeyError:
            raise BadServerConfiguration("DATETIME_FORMAT")
        except ValueError:
            raise UnsupportedDatetimeFormatError(datetime_format)

    def build(self):
        return TodoEntry(self._user_id, self._title, self._date_time)
