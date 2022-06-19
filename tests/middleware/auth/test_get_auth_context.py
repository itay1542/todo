import pytest

import src.middleware.auth.auth_context as auth_context
from src.middleware.auth.auth_context import get_auth_context
from src.middleware.exceptions.auth.user_not_logged_in_error import \
    UserNotLoggedInError


@pytest.fixture
def mock_current_app(mocker):
    mock_current_app = mocker.Mock()
    mock_current_app.config = {"AUTH_COOKIE_KEY": "a"}
    mocker.patch.object(auth_context, "current_app", mock_current_app)
    return mock_current_app


@pytest.fixture
def mock_request(mocker):
    mock_request = mocker.Mock()
    mock_request.cookies = {}
    mocker.patch.object(auth_context, "request", mock_request)
    return mock_request


class TestGetAuthContext:
    def test_returns_value_of_request_cookie(self, mock_current_app, mock_request):
        expected_cookie_value = 1
        mock_request.cookies["a"] = expected_cookie_value

        actual_context_value = get_auth_context()
        assert actual_context_value == expected_cookie_value

    def test_throws_auth_error_on_missing_cookie(self, mock_current_app, mock_request):
        mock_request.cookies = {}
        with pytest.raises(UserNotLoggedInError):
            get_auth_context()
