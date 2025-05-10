from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemSchema
from app.utils.error_handlers import NotFoundError, ValidationError, AuthError


class ItemResource(Resource):
    """Item resource for handling single item operations."""
    
    @jwt_required()
    def get(self, item_id):
        """Get a single item by ID."""
        item = Item.query.get(item_id)
        if not item:
            raise NotFoundError(f"Item with ID {item_id} not found")
        
        # Check if user has access to this item
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if item.user_id != current_user_id and not current_user.admin:
            raise AuthError("Not authorized to access this resource")
        
        return ItemSchema().dump(item), 200
    
    @jwt_required()
    def put(self, item_id):
        """Update a single item."""
        # Check authorization
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        item = Item.query.get(item_id)
        if not item:
            raise NotFoundError(f"Item with ID {item_id} not found")
        
        if item.user_id != current_user_id and not current_user.admin:
            raise AuthError("Not authorized to access this resource")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Prevent changing ownership unless admin
        if 'user_id' in json_data and json_data['user_id'] != item.user_id and not current_user.admin:
            raise AuthError("Not authorized to change item ownership")
        
        # Validate and update
        try:
            # Partial update (don't require all fields)
            schema = ItemSchema(partial=True)
            data = schema.load(json_data)
            
            # Update item attributes
            for key, value in data.items():
                setattr(item, key, value)
            
            db.session.commit()
            
            return ItemSchema().dump(item), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, item_id):
        """Delete an item."""
        # Check authorization
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        item = Item.query.get(item_id)
        if not item:
            raise NotFoundError(f"Item with ID {item_id} not found")
        
        if item.user_id != current_user_id and not current_user.admin:
            raise AuthError("Not authorized to delete this item")
        
        db.session.delete(item)
        db.session.commit()
        
        return {"message": f"Item with ID {item_id} deleted successfully"}, 200


class ItemListResource(Resource):
    """Item resource for handling multiple items."""
    
    @jwt_required()
    def get(self):
        """Get items based on user role."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Set up query
        query = Item.query
        
        # Filter by user_id if not admin
        if not current_user.admin:
            query = query.filter_by(user_id=current_user_id)
        
        # Apply additional filters if provided
        args = request.args
        if 'active' in args:
            active = args['active'].lower() == 'true'
            query = query.filter_by(active=active)
        
        items = query.all()
        return ItemSchema(many=True).dump(items), 200
    
    @jwt_required()
    def post(self):
        """Create a new item."""
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Get current user
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Only admin can create items for other users
        if 'user_id' in json_data and json_data['user_id'] != current_user_id and not current_user.admin:
            raise AuthError("Not authorized to create items for other users")
        
        # Set owner to current user if not specified
        if 'user_id' not in json_data:
            json_data['user_id'] = current_user_id
        
        # Validate and deserialize input
        try:
            item_data = ItemSchema().load(json_data)
            
            # Save the new item
            db.session.add(item_data)
            db.session.commit()
            
            return ItemSchema().dump(item_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e)) 