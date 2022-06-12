from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.data_access.models.user_model import User
from src.middleware.auth.auth_store import AuthStore
from src.middleware.exc.auth.incorrect_credentials_error import IncorrectCredentialsError
from src.middleware.exc.auth.user_already_exists_error import UserAlreadyExistsError
from src.middleware.exc.auth.user_not_found_error import UserNotFoundError

from tests.fixtures import mock_user

class TestAuthStore:
    db_session_mock = Mock()
    auth_store = AuthStore(db_session_mock)

    def test_create_user_adds_new_user_to_db_session(self):
        username, password = "1", "2"
        user = User(username, password)
        self.auth_store.create_user(user)
        self.db_session_mock.add.assert_called_with(user)
        self.db_session_mock.commit.assert_called_once()

    def test_create_user_raises_error_when_user_already_exists(self):
        username, password = "1", "2"
        self.db_session_mock.commit.side_effect = IntegrityError("something", "123", "1")
        with pytest.raises(UserAlreadyExistsError):
            self.auth_store.create_user(User(username, password))

    def test_get_user_returns_user_after_verify_password_returns_true(self, mock_user):
        mock_user.verify_password.return_value = True
        self.db_session_mock.query.return_value = mock_user

        assert self.auth_store.get_user('1', '2') == mock_user

    def test_get_user_raises_incorrect_credentials_error_when_verify_password_returns_false(self, mock_user):
        mock_user.verify_password.return_value = False
        self.db_session_mock.query.return_value = mock_user

        with pytest.raises(IncorrectCredentialsError):
            self.auth_store.get_user('1', '2')

    def test_get_user_raises_user_not_found_when_db_session_raises_no_result_found(self):
        self.db_session_mock.query.side_effect = NoResultFound()

        with pytest.raises(UserNotFoundError):
            self.auth_store.get_user('1', '2')
