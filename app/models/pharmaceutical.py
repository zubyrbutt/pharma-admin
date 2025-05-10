from datetime import datetime
from app import db


class Company(db.Model):
    """Model for pharmaceutical companies."""
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    code = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    brands = db.relationship('Brand', backref='company', lazy='dynamic')
    
    def __repr__(self):
        return f'<Company {self.name}>'


class Drug(db.Model):
    """Model for pharmaceutical drugs."""
    __tablename__ = 'drugs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    brands = db.relationship('Brand', secondary='brand_drugs', backref='drugs')
    adult_dosages = db.relationship('AdultDosage', backref='drug', lazy='dynamic')
    pediatric_dosages = db.relationship('PediatricDosage', backref='drug', lazy='dynamic')
    neonatal_dosages = db.relationship('NeonatalDosage', backref='drug', lazy='dynamic')
    
    def __repr__(self):
        return f'<Drug {self.name}>'


class Brand(db.Model):
    """Model for pharmaceutical brands."""
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    strength = db.Column(db.String(100), nullable=True)
    form = db.Column(db.String(100), nullable=True)
    package_size = db.Column(db.String(100), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Brand {self.name}>'


# Association table for many-to-many relationship between Brand and Drug
brand_drugs = db.Table('brand_drugs',
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'), primary_key=True),
    db.Column('drug_id', db.Integer, db.ForeignKey('drugs.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class AdultDosage(db.Model):
    """Model for adult dosage information."""
    __tablename__ = 'adult_dosages'
    
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False)
    indication = db.Column(db.Text, nullable=True)
    dosage = db.Column(db.Text, nullable=True)
    frequency = db.Column(db.String(100), nullable=True)
    route = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdultDosage for Drug ID {self.drug_id}>'


class PediatricDosage(db.Model):
    """Model for pediatric dosage information."""
    __tablename__ = 'pediatric_dosages'
    
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False)
    indication = db.Column(db.Text, nullable=True)
    dosage = db.Column(db.Text, nullable=True)
    age_range = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), nullable=True)
    route = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PediatricDosage for Drug ID {self.drug_id}>'


class NeonatalDosage(db.Model):
    """Model for neonatal dosage information."""
    __tablename__ = 'neonatal_dosages'
    
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False)
    indication = db.Column(db.Text, nullable=True)
    dosage = db.Column(db.Text, nullable=True)
    age_range = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), nullable=True)
    route = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<NeonatalDosage for Drug ID {self.drug_id}>' 