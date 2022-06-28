from src.common.todo_exception import TodoException


class UserNotLoggedInError(TodoException):
    def __init__(self):
        super().__init__(error_code=401)
