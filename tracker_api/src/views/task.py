from http import HTTPStatus

from flask import Response, jsonify, request, views
from flask_sqlalchemy.pagination import QueryPagination
from marshmallow.exceptions import ValidationError

from models import Item
from schemas import ItemSchema
from utils import db
from utils.decorators import TokenAuthentication


class ItemListView(views.MethodView):
    """Item List View"""

    decorators = [TokenAuthentication()]
    model = Item
    schema_class = ItemSchema

    def filter_query(self):
        """Perform filtering and ordering."""
        filter_kwargs = {"user_id": request.user.id}
        status_options = {str(s.value): s.name for s in self.model.Status}
        status = request.args.get("status")
        if status in status_options:
            filter_kwargs["status"] = status_options[status]
        order = self.model.created.asc()
        order_options = ("created", "-created")
        order_by = request.args.get("order")
        if order_by in order_options and order_by != "created":
            order = self.model.created.desc()
        query = self.model.query.filter_by(**filter_kwargs).order_by(order)
        return query

    @staticmethod
    def paginate(query):
        """Paginate if parameters allow."""
        page = request.args.get("page")
        per_page = request.args.get("per_page")

        if not page or not per_page:
            return query
        if not page.isdigit() or not per_page.isdigit():
            return query

        return query.paginate(page=int(page), per_page=int(per_page))

    def get(self, *args, **kwargs):
        """List all Task Items."""
        schema = self.schema_class(many=True)
        objects = self.paginate(self.filter_query())
        if isinstance(objects, QueryPagination):
            return {
                "count": objects.total,
                "has_prev": objects.has_prev,
                "has_next": objects.has_next,
                "results": schema.dump(objects),
            }

        return jsonify(schema.dump(objects)), HTTPStatus.OK

    def post(self, *args, **kwargs):
        """Create new Task Item."""
        schema = self.schema_class()
        try:
            instance = schema.load(request.json)
            instance.user_id = request.user.id
            db.session.add(instance)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        return jsonify(schema.dump(instance)), HTTPStatus.CREATED


class ItemDetailView(views.MethodView):
    """Item Detail View"""

    decorators = [TokenAuthentication()]
    lookup_field = "id"
    lookup_url_kwarg = None
    model = Item
    schema_class = ItemSchema

    def get_object(self, *args, **kwargs):
        """Find Task Item by ID for the Current User."""
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            "user_id": request.user.id,
            self.lookup_field: kwargs[lookup_url_kwarg],
        }
        obj = self.model.query.filter_by(**filter_kwargs).first()
        return obj

    def get(self, *args, **kwargs):
        """Retrieve Task Item by ID."""
        obj = self.get_object(*args, **kwargs)
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        schema = self.schema_class()
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def put(self, *args, **kwargs):
        """Update Task Item by ID."""
        obj = self.get_object(*args, **kwargs)
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        schema = self.schema_class()
        try:
            schema.load(request.json, instance=obj, partial=False)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def patch(self, *args, **kwargs):
        """Partial Update Task Item by ID."""
        obj = self.get_object(*args, **kwargs)
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        schema = self.schema_class()
        try:
            schema.load(request.json, instance=obj, partial=True)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def delete(self, *args, **kwargs):
        """Destroy Task Item by ID."""
        obj = self.get_object(*args, **kwargs)
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        db.session.delete(obj)
        db.session.commit()
        return Response(status=HTTPStatus.NO_CONTENT)
