from marshmallow import Schema, fields, validate, post_load
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage


class CompanySchema(Schema):
    """Schema for Company model."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    code = fields.Str(validate=validate.Length(max=50))
    address = fields.Str()
    country = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_company(self, data, **kwargs):
        """Create a Company instance from validated data."""
        return Company(**data)


class DrugSchema(Schema):
    """Schema for Drug model."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str()
    category = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_drug(self, data, **kwargs):
        """Create a Drug instance from validated data."""
        return Drug(**data)


class BrandSchema(Schema):
    """Schema for Brand model."""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    strength = fields.Str(validate=validate.Length(max=100))
    form = fields.Str(validate=validate.Length(max=100))
    package_size = fields.Str(validate=validate.Length(max=100))
    company_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_brand(self, data, **kwargs):
        """Create a Brand instance from validated data."""
        return Brand(**data)


class AdultDosageSchema(Schema):
    """Schema for AdultDosage model."""
    
    id = fields.Int(dump_only=True)
    drug_id = fields.Int(required=True)
    indication = fields.Str()
    dosage = fields.Str()
    frequency = fields.Str(validate=validate.Length(max=100))
    route = fields.Str(validate=validate.Length(max=100))
    notes = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_adult_dosage(self, data, **kwargs):
        """Create an AdultDosage instance from validated data."""
        return AdultDosage(**data)


class PediatricDosageSchema(Schema):
    """Schema for PediatricDosage model."""
    
    id = fields.Int(dump_only=True)
    drug_id = fields.Int(required=True)
    indication = fields.Str()
    dosage = fields.Str()
    age_range = fields.Str(validate=validate.Length(max=100))
    frequency = fields.Str(validate=validate.Length(max=100))
    route = fields.Str(validate=validate.Length(max=100))
    notes = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_pediatric_dosage(self, data, **kwargs):
        """Create a PediatricDosage instance from validated data."""
        return PediatricDosage(**data)


class NeonatalDosageSchema(Schema):
    """Schema for NeonatalDosage model."""
    
    id = fields.Int(dump_only=True)
    drug_id = fields.Int(required=True)
    indication = fields.Str()
    dosage = fields.Str()
    age_range = fields.Str(validate=validate.Length(max=100))
    frequency = fields.Str(validate=validate.Length(max=100))
    route = fields.Str(validate=validate.Length(max=100))
    notes = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @post_load
    def make_neonatal_dosage(self, data, **kwargs):
        """Create a NeonatalDosage instance from validated data."""
        return NeonatalDosage(**data) 