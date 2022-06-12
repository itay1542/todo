from sqlalchemy.exc import NoResultFound

from src.data_access.models.todo_entry import TodoEntry
from src.middleware.abstract_store import AbstractStore
from src.middleware.decorators.rollback_transaction_on_exception import rollback_transaction_on_exception


class TodoStore(AbstractStore):
    def __init__(self, db_session):
        super().__init__(db_session)

    @rollback_transaction_on_exception('_db_session')
    def save_todo(self, todo_entry: TodoEntry):
        self._db_session.add(todo_entry)
        self._db_session.commit()
        return todo_entry

    def get_all_todos(self, user_id: int):
        try:
            todos = self._db_session.query(TodoEntry) \
                .filter(TodoEntry.user_id == user_id).all()
            return todos
        except NoResultFound:
            return []

    @rollback_transaction_on_exception("_db_session")
    def delete_todo(self, id: int):
        self._db_session.query(TodoEntry).filter(TodoEntry.id == id).delete()
        self._db_session.commit()
