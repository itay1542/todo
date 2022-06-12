from src.common.todo_exception import TodoException


class IncorrectCredentialsError(TodoException):
    def __init__(self, msg: str):
        super().__init__(code=401, msg=msg)
