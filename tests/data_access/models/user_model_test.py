import pytest

import src.data_access.models.user_model as user_model
from src.data_access.models.user_model import User


@pytest.fixture
def mock_generate_password_hash(mocker):
    return mocker.patch.object(user_model, "generate_password_hash")


@pytest.fixture
def mock_check_password_hash(mocker):
    return mocker.patch.object(user_model, "check_password_hash")


@pytest.fixture
def user(mock_generate_password_hash, mock_check_password_hash):
    mock_generate_password_hash.return_value = "hash"
    return User("username", "password")


class TestUserPassword:
    def test_throws_error_when_trying_to_access_password(self, user):
        with pytest.raises(AttributeError):
            user.password

    def test_calls_generate_password_hash_on_given_password(
        self, user, mock_generate_password_hash
    ):
        mock_generate_password_hash.return_value = "hash"

        actual_hash = user.password_hash

        assert actual_hash == mock_generate_password_hash.return_value


class TestVerifyPassword:
    @pytest.mark.parametrize(
        "password,verification_result", [("password", True), ("password1", False)]
    )
    def test_verify_password_returns_true_when_given_password_equals_init_password(
        self, password, verification_result, user, mock_check_password_hash
    ):
        mock_check_password_hash.return_value = verification_result
        is_verified = user.verify_password(input)

        assert is_verified is verification_result


class TestUserSerialization:
    def test_hides_password_when_serializing(self, user):
        actual_dict = user.serialize()

        assert actual_dict == {"username": user.username}
