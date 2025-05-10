from marshmallow import Schema, fields, validate, post_load, validates, ValidationError
from app.models.user import User


class UserSchema(Schema):
    """Schema for User model."""
    
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    active = fields.Bool(dump_only=True)
    admin = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('username')
    def validate_username(self, value):
        """Validate username is unique."""
        user = User.query.filter_by(username=value).first()
        if user:
            raise ValidationError('Username already exists.')
    
    @validates('email')
    def validate_email(self, value):
        """Validate email is unique."""
        user = User.query.filter_by(email=value).first()
        if user:
            raise ValidationError('Email already exists.')
    
    @post_load
    def make_user(self, data, **kwargs):
        """Create a User instance from validated data."""
        return User(**data) 