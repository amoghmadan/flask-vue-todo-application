from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from utils import db


class User(db.Model):
    """User Model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    token = db.relationship("Token", backref="token", uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        stored_hash = check_password_hash(self.password, password)
        generated_hash = generate_password_hash(password)
        current_hash = check_password_hash(generated_hash, password)
        return stored_hash == current_hash

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)
