"""Various auxiliary utility methods."""

import json
from typing import Union, Dict, List, Optional

from redis import Redis
from sqlalchemy import create_engine

from src import settings

db_engine = create_engine(settings.DATABASE_URL)
redis_cli: Redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def cache_result(key: str):
    """Decorator function which caches inner func result in redis."""

    def decorator(func):

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            redis_cli.set(key, json.dumps(result), ex=redis_expire())

            return result

        return wrapper

    return decorator


def from_cache(key) -> Optional[Union[Dict, List]]:
    """Returns cached data from redis."""
    cache: Optional[bytes] = redis_cli.get(key)

    if cache:
        return json.loads(cache)

    return None


def redis_expire() -> int:
    """Returns expiration time for redis."""
    return settings.TIME_INTERVAL * 60
