from contextlib import contextmanager


@contextmanager
def simple_lock(redis_store, key, ex=None):
    is_exist = redis_store.set(key, '1', ex=ex, nx=True)
    yield is_exist
    redis_store.delete(key)
