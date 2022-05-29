from flask_restful import Resource
from flask import abort

from src.common.todo_exception import TodoException
from src.middleware.auth.auth_context import get_auth_context
from src.middleware.todo_store import TodoStore


class TodoResource(Resource):
    def __init__(self, todo_store: TodoStore):
        self._todo_store = todo_store

    def delete(self, id: int):
        try:
            get_auth_context()
            self._todo_store.delete_todo(id)
        except TodoException as e:
            abort(e.code, e)