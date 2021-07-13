from datetime import timedelta

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string

from .admin import APIKeyAdmin
from .models import APIKey
from .security import check_apikey, generate_key


def test_apikey_validation():
    key = APIKey()
    assert key
    assert key.is_valid
    key.revoked = True
    assert not key.is_valid
    key.revoked = False
    assert key.is_valid
    key.expires_at = timezone.now() - timedelta(minutes=1)
    assert not key.is_valid
    key.expires_at = timezone.now() + timedelta(minutes=1)
    assert key.is_valid
    key.expires_at = None
    assert key.is_valid


def test_key_generation():
    data = generate_key()
    assert data
    assert data.prefix
    assert data.key
    assert data.hashed_key
    assert check_password(data.key, data.hashed_key)


@pytest.mark.django_db
def test_apikey_check():
    assert not check_apikey(None)
    user = User()
    user.name = get_random_string(10)
    user.password = get_random_string(10)
    user.save()
    assert user
    key = APIKey()
    key.user = user
    key_data = generate_key()
    key.prefix = key_data.prefix
    key.hashed_key = key_data.hashed_key
    key.save()
    assert key
    assert not check_apikey(key_data.key)
    assert not check_apikey(key.prefix)
    assert not check_apikey(f"{key_data.prefix}.{get_random_string(10)}")
    assert check_apikey(f"{key_data.prefix}.{key_data.key}")
    user.is_active = False
    user.save()
    assert not check_apikey(f"{key_data.prefix}.{key_data.key}")
    user.delete()
    assert not check_apikey(f"{key_data.prefix}.{key_data.key}")


@pytest.mark.django_db
def test_admin_save():
    admin_site = AdminSite()
    apikey_admin = APIKeyAdmin(APIKey, admin_site=admin_site)
    assert admin_site
    assert apikey_admin
    user = User()
    user.name = get_random_string(10)
    user.password = get_random_string(10)
    user.save()
    assert user
    key = APIKey()
    key.user = user
    key = apikey_admin.save_model(request=None, obj=key, form=None, change=None)
    assert key
    assert key.prefix
    assert key.hashed_key
    assert key.user == user
