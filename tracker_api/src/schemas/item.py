from models import Item
from utils import ma


class ItemSchema(ma.SQLAlchemyAutoSchema):
    """Item Schema"""

    class Meta:
        model = Item
        load_instance = True
        exclude = ["user_id"]
