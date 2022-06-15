from flask import abort
from flask import request, make_response, current_app
from flask_restful import Resource, reqparse

from src.common.todo_exception import TodoException
from src.middleware.auth.auth_store import AuthStore

USERNAME_KEY = "username"
PASSWORD_KEY = "password"

parser = reqparse.RequestParser()
parser.add_argument(USERNAME_KEY, type=str)
parser.add_argument(PASSWORD_KEY, type=str)

class AuthResource(Resource):
    def __init__(self, auth_store: AuthStore):
        self._auth_store = auth_store

    def post(self):
        args = parser.parse_args(strict=True)
        try:
            username, password = args[USERNAME_KEY], args[PASSWORD_KEY]
            user_id = self._auth_store.create_user(username, password)
            return self._generate_response_with_user_cookie(user_id)
        except TodoException as e:
            abort(e.code, e)
        except KeyError as e:
            abort(400, e)

    def get(self):
        args = request.args
        try:
            username, password = args[USERNAME_KEY], args[PASSWORD_KEY]
            user = self._auth_store.get_user(username, password)
            return self._generate_response_with_user_cookie(user.id)
        except TodoException as e:
            abort(e.code, e)
        except KeyError as e:
            abort(400, e)

    def _generate_response_with_user_cookie(self, cookie_value: int):
        res = make_response()
        res.set_cookie(current_app.config.get("AUTH_COOKIE_KEY"), value=str(cookie_value))
        return res
