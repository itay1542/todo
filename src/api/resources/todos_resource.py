from flask import jsonify, abort
from flask_restful import Resource, reqparse

from src.data_access.model_builders.todo_builder import TodoBuilder
from src.middleware.auth.auth_context import get_auth_context
from src.middleware.exceptions.todos import *
from src.middleware.todo_store import TodoStore

parser = reqparse.RequestParser()

parser.add_argument('datetime')
parser.add_argument('title')


class TodosResource(Resource):
    def __init__(self, todo_store: TodoStore):
        self._todo_store = todo_store

    def post(self):
        args = parser.parse_args()
        try:
            title, datetime = args['title'], args['datetime']
            user_id = get_auth_context()
            todo = TodoBuilder(user_id, title) \
                .set_date_time(datetime) \
                .build()
            inserted_entry = self._todo_store.save_todo(todo)
            return jsonify(inserted_entry.to_dict())
        except TodoException as e:
            abort(e.code, e)
        except KeyError as e:
            abort(400, e)

    def get(self):
        try:
            user_id = get_auth_context()
            entries = self._todo_store.get_all_todos(user_id)
            entries_serialized = list(map(lambda entry: entry.to_dict(), entries))
            return jsonify(entries_serialized)
        except TodoException as e:
            abort(e.code, e)
