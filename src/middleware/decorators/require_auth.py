from src.middleware.auth.auth_context import get_auth_context


def require_auth(func):
    def wrapper(self, *args, **kwargs):
        user_id = get_auth_context()
        return func(self, user_context=user_id, *args, **kwargs)

    return wrapper
