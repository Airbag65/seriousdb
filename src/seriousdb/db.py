from .cache import Cache, require_db
from .exceptions import ResourceNotFoundError


def insert(key: str, value: str, cache: Cache):
    with cache.lock:
        require_db(cache)[key] = value
    return value


def select(key: str, cache: Cache):
    with cache.lock:
        val = require_db(cache).get(key, None)
    if val is None:
        raise ResourceNotFoundError(f"No value set for key {key}")
    return val
