from flask import Flask

from cli import manage
from utils import db, ma
from routes import urlpatterns
import settings


def get_wsgi_application():
    """
    Generate and configure the Flask application.
    :return: Flask
    """
    app = Flask(__name__)
    app.config.update(
        DEBUG=settings.DEBUG,
        ENV=settings.ENV,
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
    )
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(manage)
    for url_prefix, blueprint in urlpatterns:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
    return app


# WSGI Server consumable
application = get_wsgi_application()

if __name__ == "__main__":
    """Use this to run the development server."""
    application.run()
