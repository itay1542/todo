import pytest
from sqlalchemy.exc import NoResultFound  # type: ignore

from src.data_access.models.todo_entry import TodoEntry
from src.middleware.todo_store import TodoStore


@pytest.fixture
def mock_db_session(mocker):
    return mocker.Mock()


@pytest.fixture
def todo_store(mock_db_session):
    return TodoStore(mock_db_session)


class TestSaveTodo:
    def test_adds_to_db(self, mock_db_session, todo_store):
        todo_entry = TodoEntry(1, "title")

        todo_store.save_todo(todo_entry)

        mock_db_session.add.assert_called_with(todo_entry)
        mock_db_session.commit.assert_called_once()


class TestGetAllTodos:
    def test_returns_empty_list_when_db_raises_no_result_found(
        self, mock_db_session, todo_store
    ):
        mock_db_session.query.side_effect = NoResultFound()

        actual_todos = todo_store.get_all_todos(1)

        assert actual_todos == []
