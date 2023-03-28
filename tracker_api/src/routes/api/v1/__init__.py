from flask import Blueprint

from routes.api.v1.account import account
from routes.api.v1.task import task

urlpatterns = [
    ("/account", account),
    ("/task", task),
]

v1 = Blueprint("v1", __name__)
for url_prefix, blueprint in urlpatterns:
    v1.register_blueprint(blueprint, url_prefix=url_prefix)

__all__ = ["v1"]
