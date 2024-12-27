from marshmallow import Schema, fields, validates, ValidationError


class AuthValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
