from flasgger import swag_from
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.blueprints.users.controllers import UserController

bp = Blueprint("user", __name__)


# 路由定義
@bp.route("/register", methods=["POST"])
@swag_from("../../../docs/register_account_api_spec.yaml")
def register():
    try:
        data = request.get_json()
        result = UserController.register_user(data)
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"code": "VALIDATION_ERROR", "message": e.messages}), 400


@bp.route("/login", methods=["POST"])
@swag_from("../../../docs/login_api_spec.yaml")
def login():
    try:
        data = request.get_json()
        result = UserController.login_user(data)
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"code": "VALIDATION_ERROR", "message": e.messages}), 400
