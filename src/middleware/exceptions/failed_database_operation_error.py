from src.common.todo_exception import TodoException


class FailedDatabaseOperationError(TodoException):
    def __init__(self, model_name: str, error: str):
        super().__init__(
            error_code=500,
            msg=f"database operation for {model_name} failed due to: {error}",
        )
