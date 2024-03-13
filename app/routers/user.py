from flasgger import swag_from
from flask import Blueprint, request, jsonify

from app.services.user import register_account as register_account_service

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["POST"])
@swag_from("../../docs/account_api_spec.yaml")
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
