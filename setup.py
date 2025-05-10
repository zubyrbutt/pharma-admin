"""
Setup script to initialize the database with sample data.
Run this after setting up the application to create initial admin user and data.
"""
import os
import sys
from flask import Flask

# Adjust path to import from app directory
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.item import Item


def setup_db():
    """Initialize database with sample data."""
    app = create_app('development')
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password='adminpass',
                admin=True
            )
            db.session.add(admin)
            
            # Create regular user
            user = User(
                username='user',
                email='user@example.com',
                password='userpass'
            )
            db.session.add(user)
            
            db.session.commit()
            
            # Create sample items
            items = [
                Item(
                    name='Sample Item 1',
                    description='This is a sample item',
                    price=19.99,
                    quantity=10,
                    user_id=admin.id
                ),
                Item(
                    name='Sample Item 2',
                    description='Another sample item',
                    price=29.99,
                    quantity=5,
                    user_id=admin.id
                ),
                Item(
                    name='User Item',
                    description='An item from regular user',
                    price=15.99,
                    quantity=3,
                    user_id=user.id
                )
            ]
            
            db.session.add_all(items)
            db.session.commit()
            
            print("Database initialized with sample data.")
        else:
            print("Admin user already exists. No changes made.")


if __name__ == '__main__':
    setup_db() 