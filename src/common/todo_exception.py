class TodoException(Exception):
    def __init__(self, msg: str = None, error_code: int = 500):
        super().__init__(msg)
        self._code = error_code

    @property
    def code(self):
        return self._code
