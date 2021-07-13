from functools import lru_cache

from ninja.security import APIKeyHeader

from .security import check_apikey


class APIKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        user = check_apikey(key)

        if not user:
            return False

        request.user = user
        return user


@lru_cache
def apikey_auth():
    return APIKeyAuth()
