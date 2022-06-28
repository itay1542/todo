def rollback_transaction_on_exception(session_attribute: str):
    def _inner(func):
        def wrapper(self, *args, **kwargs):
            session = getattr(self, session_attribute)
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                session.rollback()
                raise e

        return wrapper

    return _inner
