from unittest.mock import MagicMock

import pytest

from src.middleware.auth.auth_context import get_auth_context
from src.middleware.exceptions.auth.user_not_logged_in_error import UserNotLoggedInError

import src.middleware.auth.auth_context as auth_context


class TestGetAuthContext:

    def test_get_auth_context_returns_value_of_request_cookie(self, mocker):
        expected_cookie_value = 1
        current_app_mock = MagicMock()
        current_app_mock.config = {
            "AUTH_COOKIE_KEY": "a"
        }
        request_mock = MagicMock()
        request_mock.cookies = {
            "a": expected_cookie_value
        }
        mocker.patch.object(auth_context, 'current_app', current_app_mock)
        mocker.patch.object(auth_context, 'request', request_mock)
        assert get_auth_context() == expected_cookie_value

    def test_get_auth_context_throws_auth_error_on_missing_cookie(self, mocker):
        current_app_mock = MagicMock()
        current_app_mock.config = {
            "AUTH_COOKIE_KEY": "a"
        }
        request_mock = MagicMock()
        request_mock.cookies = {}
        mocker.patch.object(auth_context, 'current_app', current_app_mock)
        mocker.patch.object(auth_context, 'request', request_mock)
        with pytest.raises(UserNotLoggedInError):
            get_auth_context()
