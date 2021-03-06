from src.common.todo_exception import TodoException


class UserAlreadyExistsError(TodoException):
    def __init__(self, msg: str = None):
        super().__init__(error_code=409, msg=msg)
