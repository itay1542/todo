from datetime import datetime

import src.data_access.models.user_model as user_model
from src.data_access.models.todo_entry import TodoEntry


class TestSerialize:
    def test_serialize_calls_to_nested_users_serialize(self, mocker):
        mock_user = mocker.patch.object(user_model, "User")
        mock_user.serialize.return_value = {}
        expected_serialized_todo = {
            "title": "title",
            "id": None,
            "date_time": datetime.now(),
            "user": {},
            "user_id": 1,
        }
        todo = TodoEntry(
            expected_serialized_todo["user_id"],
            expected_serialized_todo["title"],
            expected_serialized_todo["date_time"],
        )
        todo.user = mock_user
        actual = todo.serialize()
        assert actual == expected_serialized_todo
