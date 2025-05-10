import os
import sys
from werkzeug.security import generate_password_hash
from flask_migrate import upgrade

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.item import Item
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage

def init_db():
    """Initialize the database with migrations and seed data."""
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    
    with app.app_context():
        # Run migrations
        upgrade()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@example.com',
                username='admin',
                password='adminpassword',  # This will be hashed by the setter
                admin=True
            )
            db.session.add(admin)
            
            # Add some sample items
            item1 = Item(name='Sample Item 1', description='This is a sample item', user=admin)
            item2 = Item(name='Sample Item 2', description='This is another sample item', user=admin)
            db.session.add(item1)
            db.session.add(item2)
            
            # Add sample pharmaceutical data
            company1 = Company(name='PharmaCorp', code='PC', description='A pharmaceutical company')
            db.session.add(company1)
            
            drug1 = Drug(name='Ibuprofen', description='Anti-inflammatory drug')
            db.session.add(drug1)
            
            brand1 = Brand(
                name='BrandIbu', 
                drug=drug1, 
                company=company1, 
                strength='200mg',
                form='Tablet'
            )
            db.session.add(brand1)
            
            # Commit changes
            db.session.commit()
            print("Database initialized with seed data.")
        else:
            print("Admin user already exists. Database initialization skipped.")

if __name__ == '__main__':
    init_db() 