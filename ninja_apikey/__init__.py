from functools import lru_cache

from .security import APIKeyAuth


@lru_cache
def apikey_auth():
    return APIKeyAuth()
