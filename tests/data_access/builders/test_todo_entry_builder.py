from datetime import datetime
from unittest.mock import patch

import pytest

from src.data_access.builders.todo_builder import TodoBuilder
from src.middleware.exc.todos import BadServerConfiguration


class TestTodoEntryBuilder:

    @patch("src.data_access.builders.todo_builder.get_config", return_value={"DATETIME_FORMAT": "something"})
    @patch("src.data_access.builders.todo_builder.dt")
    def test_set_date_time_parses_string_with_configured_format(self, mocked_datetime, mocked_get_config):
        expected_datetime_parsed = datetime.today()
        mocked_datetime.strptime.return_value = expected_datetime_parsed
        builder = TodoBuilder(1, "title").set_date_time("some date time")

        assert builder.build().date_time == expected_datetime_parsed
        mocked_datetime.strptime.assert_called_with("some date time", "something")

    @patch("src.data_access.builders.todo_builder.get_config", return_value={})
    @patch("src.data_access.builders.todo_builder.dt")
    def test_set_date_throws_bad_server_configuration_server_on_missing_configuration(self, mocked_datetime, mocked_get_config):
        with pytest.raises(BadServerConfiguration):
            TodoBuilder(1, "title").set_date_time("something")