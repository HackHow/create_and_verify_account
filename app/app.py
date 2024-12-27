from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.blueprints.users.routes import bp as user_bp
from app.configs.config import get_config
from app.extensions.database import db
from app.extensions.logger import logger
from app.middlewares.error_handler import error_handler_middleware


def create_app():
    app = Flask(__name__)
    CORS(app)

    config = get_config()
    app.config.from_object(config)
    JWTManager(app)

    db.init_app(app)
    db.create_all(app)
    logger.init_app(app)
    error_handler_middleware.init_app(app)

    # 註冊 Blueprint
    app.register_blueprint(user_bp, url_prefix=f"/api/{app.config['API_VERSION']}/user")

    Swagger(app)

    @app.route("/")
    def index():
        return "Hello, World!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
