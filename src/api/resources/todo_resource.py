from flask import abort
from flask_restful import Resource

from src.common.todo_exception import TodoException
from src.middleware.decorators.require_auth import require_auth
from src.middleware.todo_store import TodoStore


class TodoResource(Resource):
    def __init__(self, todo_store: TodoStore):
        self._todo_store = todo_store

    @require_auth
    def delete(self, id: int):
        try:
            self._todo_store.delete_todo(id)
        except TodoException as e:
            abort(e.code, e)
