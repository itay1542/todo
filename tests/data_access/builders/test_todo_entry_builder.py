from datetime import datetime

import pytest

from src.data_access.model_builders.todo_builder import TodoBuilder
from src.middleware.exceptions.todos import BadServerConfiguration

import src.data_access.model_builders.todo_builder as todo_builder

class TestTodoEntryBuilder:

    def test_set_date_time_parses_string_with_configured_format(self, mocker):
        mocker.patch.object(todo_builder,"get_config", return_value={"DATETIME_FORMAT": "something"})
        expected_datetime_parsed = datetime.today()
        mocked_datetime = mocker.patch.object(todo_builder,"dt")
        mocked_datetime.strptime.return_value = expected_datetime_parsed
        builder = TodoBuilder(1, "title").set_date_time("some date time")

        assert builder.build().date_time == expected_datetime_parsed
        mocked_datetime.strptime.assert_called_with("some date time", "something")

    def test_set_date_throws_bad_server_configuration_server_on_missing_configuration(self, mocker):
        mocker.patch.object(todo_builder,"dt")
        mocker.patch.object(todo_builder,"get_config", return_value={})
        with pytest.raises(BadServerConfiguration):
            TodoBuilder(1, "title").set_date_time("something")
