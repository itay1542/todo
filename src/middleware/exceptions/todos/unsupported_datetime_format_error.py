from src.common.todo_exception import TodoException


class UnsupportedDatetimeFormatError(TodoException):
    def __init__(self, supported_format: str):
        super().__init__(
            f"received datetime format is not supported"
            f", please use: {supported_format}",
            error_code=400,
        )
