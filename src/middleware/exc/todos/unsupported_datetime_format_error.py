from src.common.todo_exception import TodoException


class UnsupportedDatetimeFormatError(TodoException):
    def __init__(self, supported_format):
        super().__init__(F"received datetime format is not supported"
                         F", please use: {supported_format}", code=400)
