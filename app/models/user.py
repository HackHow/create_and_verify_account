from psycopg2 import IntegrityError

from app.utils.db import get_db


def register_account(username, password):
    db = get_db()
    cursor = db.cursor()

    try:
        postgres_insert_query = """INSERT INTO accounts (username, password) VALUES (%s, %s) RETURNING user_id"""
        record_to_insert = (username, password)

        cursor.execute(postgres_insert_query, record_to_insert)

        user_id = cursor.fetchone()[0]
        db.commit()

        return user_id, None
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e)

        if "duplicate key value violates unique constraint" in error_msg:
            return None, "Username already exists"
        else:
            return None, "Registration failed due to a database error."
    finally:
        cursor.close()
