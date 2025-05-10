from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.schemas.user import UserSchema
from app.utils.error_handlers import NotFoundError, ValidationError, AuthError


class UserResource(Resource):
    """User resource for handling single user operations."""
    
    @jwt_required()
    def get(self, user_id):
        """Get a single user by ID."""
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Check if user is requesting their own info or is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user_id != user_id and not current_user.admin:
            raise AuthError("Not authorized to access this resource")
        
        return UserSchema().dump(user), 200
    
    @jwt_required()
    def put(self, user_id):
        """Update a single user."""
        # Check authorization
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user_id != user_id and not current_user.admin:
            raise AuthError("Not authorized to access this resource")
        
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Remove sensitive fields that shouldn't be updated via API
        if 'admin' in json_data and not current_user.admin:
            del json_data['admin']
        
        # Validate and update
        try:
            # Partial update (don't require all fields)
            schema = UserSchema(partial=True)
            data = schema.load(json_data)
            
            # Update user attributes
            for key, value in data.items():
                setattr(user, key, value)
            
            db.session.commit()
            
            return UserSchema().dump(user), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, user_id):
        """Delete a user."""
        # Check authorization
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user_id != user_id and not current_user.admin:
            raise AuthError("Not authorized to access this resource")
        
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": f"User with ID {user_id} deleted successfully"}, 200


class UserListResource(Resource):
    """User resource for handling multiple users."""
    
    @jwt_required()
    def get(self):
        """Get all users."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privilege required")
        
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200
    
    def post(self):
        """Create a new user."""
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and deserialize input
        try:
            user_data = UserSchema().load(json_data)
            
            # Save the new user
            db.session.add(user_data)
            db.session.commit()
            
            return UserSchema().dump(user_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


class UserLoginResource(Resource):
    """Resource for user login."""
    
    def post(self):
        """Login a user."""
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Check required fields
        if 'email' not in json_data or 'password' not in json_data:
            raise ValidationError("Email and password are required")
        
        # Find user by email
        user = User.query.filter_by(email=json_data['email']).first()
        if not user or not user.verify_password(json_data['password']):
            raise AuthError("Invalid email or password")
        
        # Check if user is active
        if not user.active:
            raise AuthError("User account is disabled")
        
        # Generate access token
        access_token = create_access_token(identity=user.id)
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": UserSchema().dump(user)
        }, 200 