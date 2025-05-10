#!/usr/bin/env python3
"""
Database initialization script
This script creates all database tables and an initial admin user
"""

import os
import sys

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.item import Item

def init_database(admin_username='admin', admin_email='admin@example.com', admin_password='admin123'):
    """Initialize the database and create admin user"""
    print("=== Initializing Database ===")
    
    # Create Flask app with application context
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if admin user exists
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            print(f"\nCreating admin user ({admin_email})...")
            admin = User(
                username=admin_username,
                email=admin_email,
                active=True,
                admin=True
            )
            admin.password = admin_password
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully!")
        else:
            print(f"\nAdmin user {admin_email} already exists")
        
        # Display database info
        print("\n=== Database Summary ===")
        print(f"Users: {User.query.count()}")
        print(f"Items: {Item.query.count()}")

if __name__ == "__main__":
    """Run database initialization"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize database and create admin user')
    parser.add_argument('--username', help='Admin username', default='admin')
    parser.add_argument('--email', help='Admin email', default='admin@example.com')
    parser.add_argument('--password', help='Admin password', default='admin123')
    args = parser.parse_args()
    
    init_database(
        admin_username=args.username,
        admin_email=args.email,
        admin_password=args.password
    )
    
    print("\n✓ Database initialization completed!")
    print("\nYou can now run the application with: python app.py")
    print("Login at: http://localhost:5050/admin/login") 