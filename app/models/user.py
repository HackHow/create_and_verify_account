from psycopg2 import IntegrityError, Error

from app.utils.db import get_db


def register_account(username, password):
    db = get_db()
    cursor = db.cursor()

    try:
        create_table_query = """CREATE TABLE IF NOT EXISTS accounts 
            (user_id SERIAL PRIMARY KEY, 
            username VARCHAR(32) UNIQUE NOT NULL, 
            password BYTEA NOT NULL)"""
        cursor.execute(create_table_query)

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


def login(username):
    db = get_db()
    cursor = db.cursor()

    try:
        select_query = """SELECT password FROM accounts WHERE username = %s"""
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        return result[0] if result else None
    except Error as e:
        print("Database error:", e)
        return None
    finally:
        cursor.close()
