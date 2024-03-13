from flasgger import Swagger
from flask import Flask

from app.routers.user import user_bp
from app.utils.db import init_db_pool, close_db


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        init_db_pool(app)
    else:
        app.config.update(test_config)

    app.teardown_appcontext(close_db)

    app.register_blueprint(user_bp)

    # Flasgger setup
    Swagger(app)

    @app.route("/")
    def index():
        return "Hello, World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
