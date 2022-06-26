from datetime import datetime

import pytest

import src.data_access.model_builders.todo_builder as todo_builder
from src.data_access.model_builders.todo_builder import TodoBuilder
from src.middleware.exceptions.todos import BadServerConfiguration


@pytest.fixture
def mock_get_config(mocker):
    return mocker.patch.object(
        todo_builder, "get_config", return_value={"DATETIME_FORMAT": "something"}
    )


@pytest.fixture
def mock_datetime(mocker):
    return mocker.patch.object(todo_builder, "dt")


class TestSetDateTime:
    def test_parses_string_with_configured_format(self, mock_datetime, mock_get_config):
        dt, dt_format = "some date time", "something"
        expected_datetime_parsed = datetime.today()
        mock_datetime.strptime.return_value = expected_datetime_parsed
        builder = TodoBuilder(1, "title").set_date_time(dt)

        assert builder._date_time == expected_datetime_parsed
        mock_datetime.strptime.assert_called_once_with(dt, dt_format)

    def test_throws_bad_server_configuration_server_on_missing_configuration(
        self, mock_datetime, mock_get_config
    ):
        mock_get_config.return_value = {}
        with pytest.raises(BadServerConfiguration):
            TodoBuilder(1, "title").set_date_time("something")


class TestBuild:
    def test_creates_todo_without_datetime_when_internal_datetime_empty(
        self, mock_datetime, mock_get_config
    ):
        expected_title = "title"
        expected_user_id = 1
        builder = TodoBuilder(expected_user_id, expected_title)

        built_todo = builder.build()

        assert built_todo.user_id == expected_user_id
        assert built_todo.title == expected_title
        assert built_todo.date_time is None
