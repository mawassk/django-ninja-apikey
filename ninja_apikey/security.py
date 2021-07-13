from collections import namedtuple

from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string
from ninja.security import APIKeyHeader

from .models import APIKey

KeyData = namedtuple("KeyData", "prefix key hashed_key")


def generate_key() -> KeyData:
    prefix = get_random_string(8)
    key = get_random_string(56)
    hashed_key = make_password(key)
    return KeyData(prefix, key, hashed_key)


def check_apikey(api_key: str):
    if not api_key:
        return False

    if "." not in api_key:  # Check API key format ({prefix}.{key})
        return False

    data = api_key.split(".")

    prefix = data[0]
    key = data[1]

    persistent_key = APIKey.objects.filter(prefix=prefix).first()

    if not persistent_key:
        return False

    if not check_password(key, persistent_key.hashed_key):
        return False

    if not persistent_key.is_valid:
        return False

    user = persistent_key.user

    if not user:
        return False

    if not user.is_active:
        return False

    return user


class APIKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        user = check_apikey(key)

        if not user:
            return False

        request.user = user
        return user
