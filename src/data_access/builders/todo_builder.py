from src.common.get_config import get_config
from src.data_access.models.todo_entry import TodoEntry

from datetime import datetime as dt

from src.middleware.exc.todos import *


class TodoBuilder:
    datetime = None

    def __init__(self, user_id: int, title: str):
        self.user_id = user_id
        self.title = title

    def set_datetime(self, datetime: str):
        datetime_format = None
        try:
            datetime_format = get_config()["DATETIME_FORMAT"]
            datetime = dt.strptime(datetime, datetime_format)
            self.datetime = datetime
            return self
        except KeyError:
            raise BadServerConfiguration("DATETIME_FORMAT")
        except ValueError:
            raise UnsupportedDatetimeFormatError(datetime_format)

    def build(self):
        return TodoEntry(self)
