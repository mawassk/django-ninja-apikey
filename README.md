# Django Ninja APIKey - Easy to use API key authentication for Django Ninja REST Framework
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
from ninja_apikey import apikey_auth

#  ...

api = NinjaAPI()

# ...

@api.get("/secure_endpoint", auth=apikey_auth)
def secure_endpoint(request):
    return f"Hello, {request.user}!" 
```
Or secure your whole api (or a specific [router](https://django-ninja.rest-framework.com/tutorial/routers/)) with the API keys:
```Python
# api.py

from ninja import NinjaAPI
from ninja_apikey import apikey_auth

#  ...

api = NinjaAPI(auth=apikey_auth)

# ...

@api.get("/secure_endpoint")
def secure_endpoint(request):
    return f"Hello, {request.user}!" 
```
You can create now API keys from django's admin interface.

## What next?
- To support this project, please give a star on GitHub.
- For any kind of issue feel free to open an Issue.
- Contributors are welcome! Please refer to `CONTRIBUTING.md`.