import atexit
import os

from dotenv import load_dotenv
from flask import g, current_app
from psycopg2 import pool

load_dotenv()


def init_db_pool(app):
    app.config["DB_POOL"] = pool.SimpleConnectionPool(
        minconn=1, maxconn=10, dsn=os.getenv("DATABASE_URL")
    )

    # 確保應用結束時關閉連線池
    atexit.register(lambda: app.config["DB_POOL"].closeall())


def get_db():
    if "db" not in g:
        g.db = current_app.config["DB_POOL"].getconn()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        current_app.config["DB_POOL"].putconn(db)
