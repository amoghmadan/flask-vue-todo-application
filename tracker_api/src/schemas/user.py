from marshmallow import fields


from models import User
from utils import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    """User Schema"""

    email = fields.Email()
    password = fields.String(load_only=True)

    class Meta:
        model = User
        load_instance = True
