from flasgger import swag_from
from flask import Blueprint, request, jsonify

from app.services.user import (
    register_account as register_account_service,
    login as login_service,
)

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["POST"])
@swag_from("../../docs/register_account_api_spec.yaml")
def register_account():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    response = register_account_service(username, password)

    if response["success"]:
        return jsonify(response), 201
    else:
        if response.get("reason") == "Username already exists":
            return jsonify(response), 409
        else:
            return jsonify(response), 400


@user_bp.route("/login", methods=["POST"])
@swag_from("../../docs/login_api_spec.yaml")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    response = login_service(username, password)
    if response["success"]:
        return jsonify(response), 200
    else:
        if (
            response.get("reason")
            == "Too many failed attempts. Please try again in a minute."
        ):
            return jsonify(response), 429
        elif response.get("reason") == "Username does not exist.":
            return jsonify(response), 404
        elif response.get("reason") == "Invalid password.":
            return jsonify(response), 401
        else:
            return jsonify(response), 400
