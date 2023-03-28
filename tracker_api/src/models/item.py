import enum

from sqlalchemy.sql import func

from utils import db


class Item(db.Model):
    """Item Model"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String)
    done = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.key)
