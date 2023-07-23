from collections import namedtuple
from typing import Any, Optional

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest
from django.utils.crypto import get_random_string
from ninja.security import APIKeyQuery
from ninja.security import APIKeyHeader


from .models import APIKey  # type: ignore

KeyData = namedtuple("KeyData", "prefix key hashed_key")


def generate_key() -> KeyData:
    prefix = get_random_string(8)
    key = get_random_string(56)
    hashed_key = make_password(key)
    return KeyData(prefix, key, hashed_key)


def check_apikey(api_key: str, perm) -> Any:
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
    
    # Additional checking for the view permission for the user
    if perm and not user.has_perm(perm):
        return False
    return user

# Added the api key as a query option
class APIKeyAuthQuery(APIKeyQuery):
    param_name = "api_key"
    
    def __init__(self, param_name="api_key", perm="", *args, **kwargs) -> None:
        self.param_name=param_name
        self.perm = perm
        super().__init__()

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Any:
        if not key:
            return False

        user = check_apikey(key, self.perm)

        if not user:
            return False

        request.user = user
        return user


class APIKeyAuthHeader(APIKeyHeader):
    param_name = "api_key"
    
    def __init__(self, param_name="api_key", perm="", *args, **kwargs) -> None:
        self.param_name=param_name
        #Specify the key used in the url
        self.perm = perm
        #If use must have a certain permission to use thtat api
        super().__init__()

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Any:
        if not key:
            return False

        user = check_apikey(key, self.perm)

        if not user:
            return False

        request.user = user
        return user
