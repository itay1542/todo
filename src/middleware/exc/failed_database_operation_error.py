from src.common.todo_exception import TodoException


class FailedDatabaseOperationError(TodoException):
    def __init__(self, model_name: str, error: str):
        super().__init__(code=500, msg=F"database operation for {model_name} failed due to: {error}")