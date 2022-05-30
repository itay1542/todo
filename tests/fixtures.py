from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_user():
    user_mock = MagicMock()
    user_mock.one.return_value = user_mock
    user_mock.filter.return_value = user_mock
    return user_mock