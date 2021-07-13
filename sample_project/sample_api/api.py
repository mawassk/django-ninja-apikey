from ninja import NinjaAPI

from ninja_apikey.security import APIKeyAuth

auth = APIKeyAuth()

api = NinjaAPI(title="Sample API", docs_url="/", auth=auth)


@api.get("/hello")
def hello(request):
    return f"Hello, {request.user}!"
