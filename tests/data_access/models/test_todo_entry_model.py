from datetime import datetime

from src.data_access.models.todo_entry import TodoEntry


class TestTodoEntryModel:

    def test_to_dict_calls_to_nested_user_to_dict(self, mocker):
        mock_user = mocker.patch("src.data_access.models.user_model.User")
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
