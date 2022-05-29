from flask import abort
from flask import request, make_response, current_app
from flask_restful import Resource, reqparse

from src.common.todo_exception import TodoException
from src.middleware.auth.auth_store import AuthStore

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

class AuthResource(Resource):
    def __init__(self, auth_store: AuthStore):
        self._auth_store = auth_store

    def post(self):
        args = parser.parse_args()
        username, password = args['username'], args['password']
        try:
            user_id = self._auth_store.create_user(username, password)
            return self.__generate_response_with_user_cookie(user_id)
        except TodoException as e:
            abort(e.code, e)

    def get(self):
        args = request.args
        username, password = args['username'], args['password']
        try:
            user = self._auth_store.get_user(username, password)
            return self.__generate_response_with_user_cookie(user.id)
        except TodoException as e:
            abort(e.code, e)

    def __generate_response_with_user_cookie(self, cookie_value):
        res = make_response()
        res.set_cookie(current_app.config.get("AUTH_COOKIE_KEY"), value=str(cookie_value))
        return res
