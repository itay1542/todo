from src.common.todo_exception import TodoException


class BadServerConfiguration(TodoException):
    def __init__(self, missing_key: str):
        super().__init__(F"server configuration is missing a key: {missing_key}",
                         code=500)
