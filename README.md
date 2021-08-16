<div align="center">
    <h3>Django Ninja APIKey</h3>
    <em>Easy to use API key authentication for Django Ninja REST Framework</em>
</div>
<br>
<div align="center">
    <p>
        <a href="https://github.com/mawassk/django-ninja-apikey/actions/workflows/build.yml?query=branch%3Amain++" target="_blank">
            <img src="https://github.com/mawassk/django-ninja-apikey/workflows/build/badge.svg?branch=main" alt="build">
        </a>
        <a href="https://codecov.io/gh/mawassk/django-ninja-apikey" target="_blank">
            <img src="https://img.shields.io/codecov/c/github/mawassk/django-ninja-apikey?color=%2334D058" alt="coverage">
        </a>
        <a href="https://pypi.org/project/django-ninja-apikey/">
            <img src="https://img.shields.io/pypi/v/django-ninja-apikey?color=%2334D058&label=pypi%20package" alt="pypi">
        </a>
        <a href="https://github.com/psf/black" target="_blank">
            <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="black">
        </a>
    </p>
</div>

---

This is an unofficial [Django](https://github.com/django/django) app which makes it **easy** to manage API keys for the [Django Ninja REST Framework](https://github.com/vitalik/django-ninja).

**Key Features:**
- **Easy** integration in your projects
- Well integrated in the **admin interface**
- **Secure** API keys due to hashing 
- Works with the **standard** user model

## Installation

```
pip install django-ninja-apikey
```

## Usage
Add `ninja_apikey` to your installed apps in your django project:
```Python
# settings.py

INSTALLED_APPS = [
    # ...
    "ninja_apikey",
]
```
Run the included migrations:
```
python manage.py migrate
```
Secure an api endpoint with the API keys:
```Python
# api.py

from ninja import NinjaAPI
from ninja_apikey.security import APIKeyAuth

#  ...

auth = APIKeyAuth()
api = NinjaAPI()

# ...

@api.get("/secure_endpoint", auth=auth)
def secure_endpoint(request):
    return f"Hello, {request.user}!" 
```
Or secure your whole api (or a specific [router](https://django-ninja.rest-framework.com/tutorial/routers/)) with the API keys:
```Python
# api.py

from ninja import NinjaAPI
from ninja_apikey.security import APIKeyAuth

#  ...

api = NinjaAPI(auth=APIKeyAuth())

# ...

@api.get("/secure_endpoint")
def secure_endpoint(request):
    return f"Hello, {request.user}!" 
```
You can create now API keys from django's admin interface.

## License
This project is licensed under the terms of the MIT license.