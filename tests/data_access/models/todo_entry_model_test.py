import src.data_access.models.user_model as user_model
from src.data_access.models.todo_entry import TodoEntry


class TestSerialize:
    def test_serialize_calls_to_nested_users_serialize(self, mocker):
        mock_user = mocker.patch.object(user_model, "User")
        expected_serialized_todo = {
            "title": "title",
            "id": None,
            "date_time": mocker.Mock(),
            "user": mock_user.serialize.return_value,
            "user_id": 1,
        }
        todo = TodoEntry(
            expected_serialized_todo["user_id"],
            expected_serialized_todo["title"],
            expected_serialized_todo["date_time"],
        )
        todo.user = mock_user

        actual_serialized_todo = todo.serialize()

        assert actual_serialized_todo == expected_serialized_todo
