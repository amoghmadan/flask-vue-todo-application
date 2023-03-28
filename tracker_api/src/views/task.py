from http import HTTPStatus

from flask import jsonify, request, views
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

    def get(self, *args, **kwargs):
        schema = self.schema_class(many=True)
        filter_kwargs = {"user_id": request.user.id}
        objects = self.model.query.filter_by(**filter_kwargs).order_by(self.model.created.desc())
        return jsonify(schema.dump(objects)), HTTPStatus.OK

    def post(self, *args, **kwargs):
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
    lookup_urk_kwarg = None
    model = Item
    schema_class = ItemSchema

    def get(self, *args, **kwargs):
        schema = self.schema_class()
        lookup_url_kwarg = self.lookup_urk_kwarg or self.lookup_field
        filter_kwargs = {
            "user_id": request.user.id,
            self.lookup_field: kwargs[lookup_url_kwarg],
        }
        obj = Item.query.filter_by(**filter_kwargs).first()
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def put(self, *args, **kwargs):
        schema = self.schema_class()
        lookup_url_kwarg = self.lookup_urk_kwarg or self.lookup_field
        filter_kwargs = {
            "user_id": request.user.id,
            self.lookup_field: kwargs[lookup_url_kwarg],
        }
        obj = Item.query.filter_by(**filter_kwargs).first()
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        try:
            schema.load(request.json, instance=obj, partial=False)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def patch(self, *args, **kwargs):
        schema = self.schema_class()
        lookup_url_kwarg = self.lookup_urk_kwarg or self.lookup_field
        filter_kwargs = {
            "user_id": request.user.id,
            self.lookup_field: kwargs[lookup_url_kwarg],
        }
        obj = Item.query.filter_by(**filter_kwargs).first()
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        try:
            schema.load(request.json, instance=obj, partial=True)
            db.session.commit()
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        return jsonify(schema.dump(obj)), HTTPStatus.OK

    def delete(self, *args, **kwargs):
        lookup_url_kwarg = self.lookup_urk_kwarg or self.lookup_field
        filter_kwargs = {
            "user_id": request.user.id,
            self.lookup_field: kwargs[lookup_url_kwarg],
        }
        obj = Item.query.filter_by(**filter_kwargs).first()
        if not obj:
            return jsonify({"detail": "Not Found"}), HTTPStatus.NOT_FOUND
        self.model.query.filter_by(**filter_kwargs).delete()
        db.session.commit()
        return jsonify({}), HTTPStatus.NO_CONTENT
