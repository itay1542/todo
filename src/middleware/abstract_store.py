from abc import ABC


class AbstractStore(ABC):
    def __init__(self, db_session):
        self._db_session = db_session