from src.data_access.models.user_model import User
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.middleware.abstract_store import AbstractStore
from src.middleware.decorators.rollback_transaction_on_exception import rollback_transaction_on_exception
from src.middleware.exc.auth.incorrect_credentials_error import IncorrectCredentialsError
from src.middleware.exc.auth.user_already_exists_error import UserAlreadyExistsError
from src.middleware.exc.auth.user_not_found_error import UserNotFoundError


class AuthStore(AbstractStore):
    def __init__(self, db_session):
        super().__init__(db_session)

    @rollback_transaction_on_exception('_db_session')
    def create_user(self, username: str, password: str) -> int:
        user_record = User(username, password)
        try:
            self._db_session.add(user_record)
            self._db_session.flush()
            id = user_record.id
            self._db_session.commit()
            return id
        except IntegrityError:
            raise UserAlreadyExistsError(F"username {username} already exists and cannot be created")
        except Exception as e:
            raise e

    def get_user(self, username: str, password: str):
        try:
            user = self._db_session.query(User)\
                .filter(User.username == username).one()
            if user.verify_password(password):
                return user
            else:
                raise IncorrectCredentialsError(F"incorrect credentials for user: ${username}")
        except NoResultFound:
            raise UserNotFoundError()
