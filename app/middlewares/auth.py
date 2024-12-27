from functools import wraps

from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


class AuthMiddleware:
    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                g.user_id = get_jwt_identity()
                return f(*args, **kwargs)
            except Exception as e:
                return (
                    jsonify(
                        {"code": "UNAUTHORIZED", "message": "Invalid or missing token"}
                    ),
                    401,
                )

        return decorator


auth_middleware = AuthMiddleware()
