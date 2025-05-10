from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage
from app.schemas.pharmaceutical import (
    CompanySchema, DrugSchema, BrandSchema,
    AdultDosageSchema, PediatricDosageSchema, NeonatalDosageSchema
)
from app.utils.error_handlers import NotFoundError, ValidationError, AuthError


# Company resources
class CompanyResource(Resource):
    """Resource for individual company operations."""
    
    @jwt_required()
    def get(self, company_id):
        """Get a company by ID."""
        company = Company.query.get(company_id)
        if not company:
            raise NotFoundError(f"Company with ID {company_id} not found")
        
        return CompanySchema().dump(company), 200
    
    @jwt_required()
    def put(self, company_id):
        """Update a company."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        company = Company.query.get(company_id)
        if not company:
            raise NotFoundError(f"Company with ID {company_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            # Partial update (don't require all fields)
            schema = CompanySchema(partial=True)
            data = schema.load(json_data)
            
            # Update company attributes
            for key, value in data.items():
                setattr(company, key, value)
            
            db.session.commit()
            
            return CompanySchema().dump(company), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, company_id):
        """Delete a company."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        company = Company.query.get(company_id)
        if not company:
            raise NotFoundError(f"Company with ID {company_id} not found")
        
        # Check if there are related brands
        if company.brands.count() > 0:
            raise ValidationError("Cannot delete company with related brands")
        
        db.session.delete(company)
        db.session.commit()
        
        return {"message": f"Company with ID {company_id} deleted successfully"}, 200


class CompanyListResource(Resource):
    """Resource for multiple company operations."""
    
    def get(self):
        """Get all companies."""
        companies = Company.query.all()
        return CompanySchema(many=True).dump(companies), 200
    
    @jwt_required()
    def post(self):
        """Create a new company."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            company_data = CompanySchema().load(json_data)
            
            db.session.add(company_data)
            db.session.commit()
            
            return CompanySchema().dump(company_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


# Drug resources
class DrugResource(Resource):
    """Resource for individual drug operations."""
    
    @jwt_required()
    def get(self, drug_id):
        """Get a drug by ID."""
        drug = Drug.query.get(drug_id)
        if not drug:
            raise NotFoundError(f"Drug with ID {drug_id} not found")
        
        return DrugSchema().dump(drug), 200
    
    @jwt_required()
    def put(self, drug_id):
        """Update a drug."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        drug = Drug.query.get(drug_id)
        if not drug:
            raise NotFoundError(f"Drug with ID {drug_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            schema = DrugSchema(partial=True)
            data = schema.load(json_data)
            
            for key, value in data.items():
                setattr(drug, key, value)
            
            db.session.commit()
            
            return DrugSchema().dump(drug), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, drug_id):
        """Delete a drug."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        drug = Drug.query.get(drug_id)
        if not drug:
            raise NotFoundError(f"Drug with ID {drug_id} not found")
        
        # Check if there are related dosages
        if drug.adult_dosages.count() > 0 or drug.pediatric_dosages.count() > 0 or drug.neonatal_dosages.count() > 0:
            raise ValidationError("Cannot delete drug with related dosages")
        
        db.session.delete(drug)
        db.session.commit()
        
        return {"message": f"Drug with ID {drug_id} deleted successfully"}, 200


class DrugListResource(Resource):
    """Resource for multiple drug operations."""
    
    def get(self):
        """Get all drugs."""
        drugs = Drug.query.all()
        return DrugSchema(many=True).dump(drugs), 200
    
    @jwt_required()
    def post(self):
        """Create a new drug."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            drug_data = DrugSchema().load(json_data)
            
            db.session.add(drug_data)
            db.session.commit()
            
            return DrugSchema().dump(drug_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


# Brand resources
class BrandResource(Resource):
    """Resource for individual brand operations."""
    
    @jwt_required()
    def get(self, brand_id):
        """Get a brand by ID."""
        brand = Brand.query.get(brand_id)
        if not brand:
            raise NotFoundError(f"Brand with ID {brand_id} not found")
        
        return BrandSchema().dump(brand), 200
    
    @jwt_required()
    def put(self, brand_id):
        """Update a brand."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        brand = Brand.query.get(brand_id)
        if not brand:
            raise NotFoundError(f"Brand with ID {brand_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            schema = BrandSchema(partial=True)
            data = schema.load(json_data)
            
            for key, value in data.items():
                setattr(brand, key, value)
            
            db.session.commit()
            
            return BrandSchema().dump(brand), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, brand_id):
        """Delete a brand."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        brand = Brand.query.get(brand_id)
        if not brand:
            raise NotFoundError(f"Brand with ID {brand_id} not found")
        
        db.session.delete(brand)
        db.session.commit()
        
        return {"message": f"Brand with ID {brand_id} deleted successfully"}, 200


class BrandListResource(Resource):
    """Resource for multiple brand operations."""
    
    def get(self):
        """Get all brands."""
        brands = Brand.query.all()
        return BrandSchema(many=True).dump(brands), 200
    
    @jwt_required()
    def post(self):
        """Create a new brand."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            brand_data = BrandSchema().load(json_data)
            
            db.session.add(brand_data)
            db.session.commit()
            
            return BrandSchema().dump(brand_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


# Dosage resources
class AdultDosageResource(Resource):
    """Resource for individual adult dosage operations."""
    
    @jwt_required()
    def get(self, dosage_id):
        """Get an adult dosage by ID."""
        dosage = AdultDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Adult dosage with ID {dosage_id} not found")
        
        return AdultDosageSchema().dump(dosage), 200
    
    @jwt_required()
    def put(self, dosage_id):
        """Update an adult dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = AdultDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Adult dosage with ID {dosage_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            schema = AdultDosageSchema(partial=True)
            data = schema.load(json_data)
            
            for key, value in data.items():
                setattr(dosage, key, value)
            
            db.session.commit()
            
            return AdultDosageSchema().dump(dosage), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, dosage_id):
        """Delete an adult dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = AdultDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Adult dosage with ID {dosage_id} not found")
        
        db.session.delete(dosage)
        db.session.commit()
        
        return {"message": f"Adult dosage with ID {dosage_id} deleted successfully"}, 200


class AdultDosageListResource(Resource):
    """Resource for multiple adult dosage operations."""
    
    def get(self):
        """Get all adult dosages."""
        # Filter by drug_id if provided
        drug_id = request.args.get('drug_id')
        if drug_id:
            dosages = AdultDosage.query.filter_by(drug_id=drug_id).all()
        else:
            dosages = AdultDosage.query.all()
        
        return AdultDosageSchema(many=True).dump(dosages), 200
    
    @jwt_required()
    def post(self):
        """Create a new adult dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            dosage_data = AdultDosageSchema().load(json_data)
            
            db.session.add(dosage_data)
            db.session.commit()
            
            return AdultDosageSchema().dump(dosage_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


# Similar resources for pediatric and neonatal dosages
class PediatricDosageResource(Resource):
    """Resource for individual pediatric dosage operations."""
    
    @jwt_required()
    def get(self, dosage_id):
        """Get a pediatric dosage by ID."""
        dosage = PediatricDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Pediatric dosage with ID {dosage_id} not found")
        
        return PediatricDosageSchema().dump(dosage), 200
    
    @jwt_required()
    def put(self, dosage_id):
        """Update a pediatric dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = PediatricDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Pediatric dosage with ID {dosage_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            schema = PediatricDosageSchema(partial=True)
            data = schema.load(json_data)
            
            for key, value in data.items():
                setattr(dosage, key, value)
            
            db.session.commit()
            
            return PediatricDosageSchema().dump(dosage), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, dosage_id):
        """Delete a pediatric dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = PediatricDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Pediatric dosage with ID {dosage_id} not found")
        
        db.session.delete(dosage)
        db.session.commit()
        
        return {"message": f"Pediatric dosage with ID {dosage_id} deleted successfully"}, 200


class PediatricDosageListResource(Resource):
    """Resource for multiple pediatric dosage operations."""
    
    def get(self):
        """Get all pediatric dosages."""
        # Filter by drug_id if provided
        drug_id = request.args.get('drug_id')
        if drug_id:
            dosages = PediatricDosage.query.filter_by(drug_id=drug_id).all()
        else:
            dosages = PediatricDosage.query.all()
        
        return PediatricDosageSchema(many=True).dump(dosages), 200
    
    @jwt_required()
    def post(self):
        """Create a new pediatric dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            dosage_data = PediatricDosageSchema().load(json_data)
            
            db.session.add(dosage_data)
            db.session.commit()
            
            return PediatricDosageSchema().dump(dosage_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))


class NeonatalDosageResource(Resource):
    """Resource for individual neonatal dosage operations."""
    
    @jwt_required()
    def get(self, dosage_id):
        """Get a neonatal dosage by ID."""
        dosage = NeonatalDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Neonatal dosage with ID {dosage_id} not found")
        
        return NeonatalDosageSchema().dump(dosage), 200
    
    @jwt_required()
    def put(self, dosage_id):
        """Update a neonatal dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = NeonatalDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Neonatal dosage with ID {dosage_id} not found")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and update
        try:
            schema = NeonatalDosageSchema(partial=True)
            data = schema.load(json_data)
            
            for key, value in data.items():
                setattr(dosage, key, value)
            
            db.session.commit()
            
            return NeonatalDosageSchema().dump(dosage), 200
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e))
    
    @jwt_required()
    def delete(self, dosage_id):
        """Delete a neonatal dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        dosage = NeonatalDosage.query.get(dosage_id)
        if not dosage:
            raise NotFoundError(f"Neonatal dosage with ID {dosage_id} not found")
        
        db.session.delete(dosage)
        db.session.commit()
        
        return {"message": f"Neonatal dosage with ID {dosage_id} deleted successfully"}, 200


class NeonatalDosageListResource(Resource):
    """Resource for multiple neonatal dosage operations."""
    
    def get(self):
        """Get all neonatal dosages."""
        # Filter by drug_id if provided
        drug_id = request.args.get('drug_id')
        if drug_id:
            dosages = NeonatalDosage.query.filter_by(drug_id=drug_id).all()
        else:
            dosages = NeonatalDosage.query.all()
        
        return NeonatalDosageSchema(many=True).dump(dosages), 200
    
    @jwt_required()
    def post(self):
        """Create a new neonatal dosage."""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user.admin:
            raise AuthError("Admin privileges required")
        
        # Get JSON data
        json_data = request.get_json()
        if not json_data:
            raise ValidationError("No input data provided")
        
        # Validate and create
        try:
            dosage_data = NeonatalDosageSchema().load(json_data)
            
            db.session.add(dosage_data)
            db.session.commit()
            
            return NeonatalDosageSchema().dump(dosage_data), 201
        
        except Exception as e:
            db.session.rollback()
            raise ValidationError(str(e)) 