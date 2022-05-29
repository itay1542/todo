from src.common.todo_exception import TodoException


class UserAlreadyExistsError(TodoException):
    def __init__(self, msg):
        super().__init__(code=409, msg=msg)