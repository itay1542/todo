from src.common.todo_exception import TodoException


class UserNotFoundError(TodoException):
    def __init__(self, msg=None):
        super().__init__(error_code=404, msg=msg)
