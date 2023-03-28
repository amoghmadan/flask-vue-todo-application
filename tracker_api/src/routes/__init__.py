from routes.api import api

urlpatterns = [
    ("/api", api),
]

__all__ = ["urlpatterns"]
