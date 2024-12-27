import re

from marshmallow import Schema, fields, validates, ValidationError


class AuthValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("username")
    def validate_username(self, value):
        if not 3 <= len(value) <= 32:
            raise ValidationError("Username length must be between 3 and 32 characters")

    @validates("password")
    def validate_password(self, value):
        if not 8 <= len(value) <= 32:
            raise ValidationError("Password length must be between 8 and 32 characters")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", value):
            raise ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number"
            )
