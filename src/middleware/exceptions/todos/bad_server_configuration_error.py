from src.common.todo_exception import TodoException


class BadServerConfiguration(TodoException):
    def __init__(self, missing_key: str):
        super().__init__(
            f"server configuration is missing a key: {missing_key}", error_code=500
        )
