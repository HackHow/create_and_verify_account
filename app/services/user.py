from time import time

import bcrypt

from app.models.user import (
    register_account as register_account_model,
    login as login_model,
)


def register_account(username, password):
    if len(username) < 3 or len(username) > 32:
        return {
            "success": False,
            "reason": "Username length must be between 3 and 32 characters",
        }

    if len(password) < 8 or len(password) > 32:
        return {
            "success": False,
            "reason": "Password length must be between 8 and 32 characters",
        }

    if not any(char.isupper() for char in password):
        return {
            "success": False,
            "reason": "Password must contain at least one uppercase letter",
        }

    if not any(char.islower() for char in password):
        return {
            "success": False,
            "reason": "Password must contain at least one lowercase letter",
        }

    if not any(char.isdigit() for char in password):
        return {
            "success": False,
            "reason": "Password must contain at least one number",
        }

    salt = bcrypt.gensalt()
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    user_id, error = register_account_model(username, hashed_password)

    if error is not None:
        return {
            "success": False,
            "reason": error,
        }
    else:
        return {
            "success": True,
        }


failed_attempts_dict = {}


def login(username, password):
    if username in failed_attempts_dict:
        last_attempt_time, attempts = failed_attempts_dict[username]
        if attempts >= 5 and (time() - last_attempt_time) < 60:
            return {
                "success": False,
                "reason": "Too many failed attempts. Please try again in a minute.",
            }

    hashed_password = login_model(username)

    if not hashed_password:
        return {"success": False, "reason": "Username does not exist."}

    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.tobytes()):
        failed_attempts_dict.pop(username, None)
        return {"success": True}
    else:
        if username in failed_attempts_dict:
            failed_attempts_dict[username] = (
                time(),
                failed_attempts_dict[username][1] + 1,
            )
        else:
            failed_attempts_dict[username] = (time(), 1)

        return {"success": False, "reason": "Invalid password."}
