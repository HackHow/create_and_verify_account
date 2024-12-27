import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    API_VERSION = os.getenv("API_VERSION", "v1")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        "swagger_ui": True,
        "specs_route": f"/api/{os.getenv('API_VERSION', 'v1')}/apidocs",
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/dev_db"
    )
    LOG_LEVEL = "DEBUG"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5432/test_db"
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    LOG_LEVEL = "ERROR"


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(env, DevelopmentConfig)
