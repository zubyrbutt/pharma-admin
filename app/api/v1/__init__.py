from flask import Blueprint, send_from_directory
from flask_restful import Api

# Create blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Import and register resources
from .resources.user import UserResource, UserListResource, UserLoginResource
from .resources.item import ItemResource, ItemListResource
from .resources.pharmaceutical import (
    CompanyResource, CompanyListResource,
    DrugResource, DrugListResource,
    BrandResource, BrandListResource,
    AdultDosageResource, AdultDosageListResource,
    PediatricDosageResource, PediatricDosageListResource,
    NeonatalDosageResource, NeonatalDosageListResource
)

# User endpoints
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserLoginResource, '/login')

# Item endpoints
api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/items/<int:item_id>')

# Pharmaceutical endpoints
api.add_resource(CompanyListResource, '/companies')
api.add_resource(CompanyResource, '/companies/<int:company_id>')
api.add_resource(DrugListResource, '/drugs')
api.add_resource(DrugResource, '/drugs/<int:drug_id>')
api.add_resource(BrandListResource, '/brands')
api.add_resource(BrandResource, '/brands/<int:brand_id>')
api.add_resource(AdultDosageListResource, '/adult-dosages')
api.add_resource(AdultDosageResource, '/adult-dosages/<int:dosage_id>')
api.add_resource(PediatricDosageListResource, '/pediatric-dosages')
api.add_resource(PediatricDosageResource, '/pediatric-dosages/<int:dosage_id>')
api.add_resource(NeonatalDosageListResource, '/neonatal-dosages')
api.add_resource(NeonatalDosageResource, '/neonatal-dosages/<int:dosage_id>')

# Add route to serve swagger.json
@api_bp.route('/swagger.json')
def swagger():
    return send_from_directory('app/static', 'swagger.json') 