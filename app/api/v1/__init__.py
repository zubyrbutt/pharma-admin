from flask import Blueprint, send_from_directory
from flask_restful import Api

# Create blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Import and register resources
from .resources.user import UserResource, UserListResource, UserLoginResource
from .resources.item import ItemResource, ItemListResource

# User endpoints
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserLoginResource, '/login')

# Item endpoints
api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/items/<int:item_id>')

# Add route to serve swagger.json
@api_bp.route('/swagger.json')
def swagger():
    return send_from_directory('app/static', 'swagger.json') 