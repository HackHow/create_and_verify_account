from flask import jsonify, request
from marshmallow import ValidationError


class ErrorHandlerMiddleware:
    @staticmethod
    def init_app(app):

        @app.errorhandler(ValidationError)
        def handle_validation_error(error):
            app.logger.warning(
                f"Validation error: {error.messages}", extra={"path": request.path}
            )
            return (
                jsonify({"code": "VALIDATION_ERROR", "message": str(error.messages)}),
                400,
            )

        @app.errorhandler(Exception)
        def handle_generic_error(error):
            app.logger.error(
                f"Unexpected error: {str(error)}",
                exc_info=True,
                extra={"path": request.path},
            )
            return (
                jsonify(
                    {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                    }
                ),
                500,
            )


error_handler_middleware = ErrorHandlerMiddleware()
