from flask import current_app, request

from src.middleware.exceptions.auth.user_not_logged_in_error import UserNotLoggedInError


def get_auth_context():
    try:
        return int(request.cookies[current_app.config["AUTH_COOKIE_KEY"]])
    except Exception:
        raise UserNotLoggedInError()
