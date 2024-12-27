from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


class Database:
    def __init__(self):
        self.db = SQLAlchemy()

    def init_app(self, app):
        self.db.init_app(app)

    def create_all(self, app):
        with app.app_context():
            # 檢查資料庫是否存在，否則創建
            engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
            if not database_exists(engine.url):
                create_database(engine.url)
            self.db.create_all()


db = Database()
