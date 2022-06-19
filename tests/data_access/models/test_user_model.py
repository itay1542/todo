import pytest

import src.data_access.models.user_model as user_model
from src.data_access.models.user_model import User


class TestUserPassword:
    def test_throws_error_when_trying_to_access_password(self):
        user = User("username", "password")
        with pytest.raises(AttributeError):
            user.password

    def test_calls_generate_password_hash_on_given_password(self, mocker):
        expected_hash = "hash"
        mocker.patch.object(
            user_model, "generate_password_hash", return_value=expected_hash
        )
        user = User("username", "password")
        actual = user.password_hash
        assert actual == expected_hash

    def test_verify_password_returns_true_when_given_password_equals_init_password(
        self,
    ):
        password = "password"
        user = User("username", password)
        is_verified = user.verify_password(password)
        assert is_verified is True

    def test_verify_password_returns_false_when_given_different_password(self):
        password = "password"
        user = User("username", password)
        wrong_password = password + "1"
        is_verified = user.verify_password(wrong_password)
        assert is_verified is False


class TestUserSerialization:
    def test_hides_password_when_serializing(self):
        expected_dict = {"username": "username"}
        user = User(expected_dict["username"], "some password")
        actual_dict = user.serialize()
        assert actual_dict == expected_dict
