class TodoException(Exception):
    def __init__(self, msg: str = None, code: int = 500):
        super().__init__(msg)
        self._code = code

    @property
    def code(self):
        return self._code