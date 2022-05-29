from flask import request, current_app

from src.middleware.exc.auth.user_not_logged_in_error import UserNotLoggedInError


def get_auth_context():
    try:
        return int(request.cookies[current_app.config["AUTH_COOKIE_KEY"]])
    except Exception:
        raise UserNotLoggedInError()
