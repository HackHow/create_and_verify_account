import bcrypt
from flask_jwt_extended import create_access_token

from app.blueprints.users.models import User


class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    @staticmethod
    def register_user(username: str, password: str):
        if User.get_by_username(username):
            return {"code": "USER_EXISTS", "message": "Username already exists"}

        hashed_password = UserService.hash_password(password)
        User.create(username=username, password=hashed_password)
        return {"code": "SUCCESS", "message": "User registered successfully"}

    @staticmethod
    def login_user(username: str, password: str):
        user = User.get_by_username(username)
        if not user or not UserService.verify_password(password, user.password):
            return {"code": "AUTH_FAILED", "message": "Invalid username or password"}

        token = create_access_token(identity=user.id)
        return {
            "code": "SUCCESS",
            "message": "Login successful",
            "data": {"token": token, "username": username},
        }
