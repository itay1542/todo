from flask import abort, jsonify
from flask_restful import Resource, reqparse

from src.data_access.model_builders.todo_builder import TodoBuilder
from src.middleware.decorators.require_auth import require_auth
from src.middleware.exceptions.todos import TodoException
from src.middleware.todo_store import TodoStore

parser = reqparse.RequestParser()

parser.add_argument("datetime")
parser.add_argument("title")


class TodosResource(Resource):
    def __init__(self, todo_store: TodoStore):
        self._todo_store = todo_store

    @require_auth
    def post(self, user_context):
        args = parser.parse_args()
        try:
            title, datetime = args["title"], args["datetime"]
            todo = TodoBuilder(user_context, title).set_date_time(datetime).build()
            inserted_entry = self._todo_store.save_todo(todo)
            return jsonify(inserted_entry.serialize())
        except TodoException as e:
            abort(e.code, e)
        except KeyError as e:
            abort(400, e)

    @require_auth
    def get(self, user_context):
        try:
            entries = self._todo_store.get_all_todos(user_context)
            entries_serialized = list(map(lambda entry: entry.serialize(), entries))
            return jsonify(entries_serialized)
        except TodoException as e:
            abort(e.code, e)
