from flask import Blueprint

from views.account import DetailView, LoginView, LogoutView

account = Blueprint("account", __name__)
account.add_url_rule("/detail", view_func=DetailView.as_view("detail"), methods=["GET"])
account.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
account.add_url_rule(
    "/logout", view_func=LogoutView.as_view("logout"), methods=["DELETE"]
)
