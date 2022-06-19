import pytest
from sqlalchemy.exc import IntegrityError, NoResultFound # type: ignore

from src.data_access.models.user_model import User
from src.middleware.auth.auth_store import AuthStore, IncorrectCredentialsError
from src.middleware.exceptions.auth.user_already_exists_error import \
    UserAlreadyExistsError
from src.middleware.exceptions.auth.user_not_found_error import \
    UserNotFoundError


@pytest.fixture
def mock_user(mocker):
    mock_user = mocker.Mock()
    mock_user.one.return_value = mock_user
    mock_user.filter.return_value = mock_user
    return mock_user


@pytest.fixture
def mock_db_session(mocker):
    return mocker.Mock()


@pytest.fixture
def auth_store(mock_db_session):
    return AuthStore(mock_db_session)


class TestCreateUser:
    def test_adds_new_user_to_db_session(self, mock_db_session, auth_store):
        username, password = "1", "2"
        user = User(username, password)
        auth_store.create_user(user)
        mock_db_session.add.assert_called_with(user)
        mock_db_session.commit.assert_called_once()

    def test_raises_error_when_user_already_exists(self, mock_db_session, auth_store):
        username, password = "1", "2"
        mock_db_session.commit.side_effect = IntegrityError("something", "123", "1")
        with pytest.raises(UserAlreadyExistsError):
            auth_store.create_user(User(username, password))


class TestGetUser:
    def test_returns_user_after_verify_password_returns_true(
        self, mock_user, mock_db_session, auth_store
    ):
        mock_user.verify_password.return_value = True
        mock_db_session.query.return_value = mock_user

        returned_user = auth_store.get_user("1", "2")
        assert returned_user == mock_user

    def test_raises_incorrect_credentials_error_when_verify_password_returns_false(
        self, mock_user, mock_db_session, auth_store
    ):
        mock_user.verify_password.return_value = False
        mock_db_session.query.return_value = mock_user

        with pytest.raises(IncorrectCredentialsError):
            auth_store.get_user("1", "2")

    def test_raises_user_not_found_when_db_session_raises_no_result_found(
        self, mock_db_session, auth_store
    ):
        mock_db_session.query.side_effect = NoResultFound()

        with pytest.raises(UserNotFoundError):
            auth_store.get_user("1", "2")
