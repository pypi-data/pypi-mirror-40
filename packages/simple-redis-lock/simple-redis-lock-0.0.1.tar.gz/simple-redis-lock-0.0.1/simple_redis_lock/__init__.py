class LockError(Exception):
    pass


class SimpleLock:
    def __init__(self, redis_store, name, ex=None):
        self.redis_store = redis_store
        self.name = name
        self.ex = ex

    def __enter__(self):
        is_exist = self.redis_store.set(self.name, '1', ex=self.ex, nx=True)
        if is_exist:
            raise LockError

    def __exit__(self, type, value, traceback):
        self.redis_store.delete(self.name)
