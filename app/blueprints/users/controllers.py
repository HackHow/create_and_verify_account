from app.blueprints.users.services.user_service import UserService
from app.utils.validators import AuthValidator


class UserController:
    @staticmethod
    def register_user(data):
        AuthValidator().load(data)
        return UserService.register_user(data["username"], data["password"])

    @staticmethod
    def login_user(data):
        AuthValidator().load(data)
        return UserService.login_user(data["username"], data["password"])
