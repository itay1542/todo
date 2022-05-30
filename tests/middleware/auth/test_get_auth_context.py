from unittest.mock import patch, MagicMock

import pytest

from src.middleware.auth.auth_context import get_auth_context
from src.middleware.exc.auth.user_not_logged_in_error import UserNotLoggedInError


class TestGetAuthContext:

    def test_get_auth_context_returns_value_of_request_cookie(self):
        expected_cookie_value = 1
        current_app_mock = MagicMock()
        current_app_mock.config = {
            "AUTH_COOKIE_KEY": "a"
        }
        request_mock = MagicMock()
        request_mock.cookies = {
            "a": expected_cookie_value
        }
        with patch('src.middleware.auth.auth_context.current_app', current_app_mock):
            with patch('src.middleware.auth.auth_context.request', request_mock):
                assert get_auth_context() == expected_cookie_value

    def test_get_auth_context_throws_auth_error_on_missing_cookie(self):
        current_app_mock = MagicMock()
        current_app_mock.config = {
            "AUTH_COOKIE_KEY": "a"
        }
        request_mock = MagicMock()
        request_mock.cookies = {}
        with patch('src.middleware.auth.auth_context.current_app', current_app_mock):
            with patch('src.middleware.auth.auth_context.request', request_mock):
                with pytest.raises(UserNotLoggedInError):
                    get_auth_context()
