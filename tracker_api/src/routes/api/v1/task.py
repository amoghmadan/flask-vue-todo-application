from flask import Blueprint

from views.task import ItemListView, ItemDetailView

task = Blueprint("task", __name__)
task.add_url_rule(
    "/items", view_func=ItemListView.as_view("item-list"), methods=["GET", "POST"]
)
task.add_url_rule(
    "/items/<int:id>",
    view_func=ItemDetailView.as_view("item-detail"),
    methods=["GET", "PUT", "PATCH", "DELETE"],
)
