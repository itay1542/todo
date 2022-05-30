from datetime import datetime
from unittest.mock import patch

from src.data_access.models.todo_entry import TodoEntry


class TestTodoEntryModel:

    @patch("src.data_access.models.user_model.User")
    def test_to_dict_calls_to_nested_user_to_dict(self, mock_user):
        mock_user.toDict.return_value = {}
        expected = {
            "title": "title",
            "id": None,
            "date_time": datetime.now(),
            "user": {},
            "user_id": 1
        }
        todo = TodoEntry(expected["user_id"], expected["title"], expected["date_time"])
        todo.user = mock_user
        assert todo.toDict() == expected
