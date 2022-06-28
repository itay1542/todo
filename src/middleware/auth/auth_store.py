from sqlalchemy.exc import IntegrityError, NoResultFound  # type: ignore

from src.common.todo_exception import TodoException
from src.data_access.models.user_model import User
from src.middleware.abstract_store import AbstractStore
from src.middleware.decorators.rollback_transaction_on_exception import (
    rollback_transaction_on_exception,
)
from src.middleware.exceptions.auth.user_already_exists_error import (
    UserAlreadyExistsError,
)
from src.middleware.exceptions.auth.user_not_found_error import UserNotFoundError


class AuthStore(AbstractStore):
    def __init__(self, db_session):
        super().__init__(db_session)

    @rollback_transaction_on_exception("_db_session")
    def create_user(self, user: User) -> int:
        try:
            self._db_session.add(user)
            self._db_session.commit()
            return user.id
        except IntegrityError:
            raise UserAlreadyExistsError(
                f"username {user.username} already exists and cannot be created"
            )
        except Exception as e:
            raise e

    def get_user(self, username: str, password: str):
        try:
            user = self._db_session.query(User).filter(User.username == username).one()
            if user.verify_password(password):
                return user
            else:
                raise IncorrectCredentialsError(
                    f"incorrect credentials for user: ${username}"
                )
        except NoResultFound:
            raise UserNotFoundError()


class IncorrectCredentialsError(TodoException):
    def __init__(self, msg: str):
        super().__init__(error_code=401, msg=msg)
