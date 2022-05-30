from unittest.mock import Mock

from sqlalchemy.exc import NoResultFound

from src.data_access.models.todo_entry import TodoEntry
from src.middleware.todo_store import TodoStore


class TestTodoStore:
    db_session_mock = Mock()
    todo_store = TodoStore(db_session_mock)

    def test_save_todo_adds_to_db(self):
        todo_entry = TodoEntry(1, 'title')
        self.todo_store.save_todo(todo_entry)
        self.db_session_mock.add.assert_called_with(todo_entry)
        self.db_session_mock.commit.assert_called_once()

    def test_get_all_todos_returns_empty_list_when_db_raises_no_result_found(self):
        self.db_session_mock.query.side_effect = NoResultFound()
        assert self.todo_store.get_all_todos(1) == []
