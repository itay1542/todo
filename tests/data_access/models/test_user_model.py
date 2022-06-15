import pytest

from src.data_access.models.user_model import User

import src.data_access.models.user_model as user_model


class TestUserModel:
    def test_throws_error_when_trying_to_access_password(self):
        user = User('username', 'password')
        with pytest.raises(AttributeError):
            password = user.password

    def test_calls_generate_password_hash_on_given_password(self, mocker):
        mocker.patch.object(user_model,'generate_password_hash', return_value="mock")
        user = User('username', 'password')
        assert user.password_hash == "mock"

    def test_verify_password_returns_true_when_given_password_equals_init_password(self):
        password = "password"
        user = User('username', password)
        assert user.verify_password(password) == True

    def test_verify_password_returns_false_when_given_different_password(self):
        password = "password"
        user = User('username', password)
        assert user.verify_password(password+"1") == False

    def test_to_dict_contains_true_values(self):
        expected = {
            "username": "username"
        }
        user = User(expected["username"], 'some password')
        assert user.to_dict() == expected
