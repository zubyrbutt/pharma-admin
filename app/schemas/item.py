from marshmallow import Schema, fields, validate, post_load
from app.models.item import Item


class ItemSchema(Schema):
    """Schema for Item model."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    quantity = fields.Int(validate=validate.Range(min=0))
    active = fields.Bool()
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_item(self, data, **kwargs):
        """Create an Item instance from validated data."""
        return Item(**data) 