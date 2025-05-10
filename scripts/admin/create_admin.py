#!/usr/bin/env python3
"""
Script to create an admin user in the database
Run this script when you need to create or reset the admin account
"""

import os
import sys

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models.user import User

def create_admin_user(username='admin', email='admin@example.com', password='admin123'):
    """Create an admin user if it doesn't exist already"""
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Check if admin exists
        existing_admin = User.query.filter_by(email=email).first()
        
        if existing_admin:
            print(f"Admin user with email '{email}' already exists!")
            
            # Update password if requested
            update = input("Do you want to reset the password? (y/n): ").lower()
            if update == 'y':
                existing_admin.password = password
                db.session.commit()
                print(f"Password updated for admin user: {username}")
            return
        
        # Create new admin user
        new_admin = User(
            username=username,
            email=email,
            active=True,
            admin=True
        )
        new_admin.password = password  # This will use the password setter which hashes it
        
        # Add to database
        db.session.add(new_admin)
        db.session.commit()
        
        print(f"Admin user created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("\nYou can now log in at http://localhost:5050/admin/login")

if __name__ == "__main__":
    print("=== Admin User Creation Tool ===\n")
    
    # Get custom values or use defaults
    use_custom = input("Use custom admin credentials? (y/n) [default: n]: ").lower()
    
    if use_custom == 'y':
        username = input("Username [default: admin]: ") or 'admin'
        email = input("Email [default: admin@example.com]: ") or 'admin@example.com'
        password = input("Password [default: admin123]: ") or 'admin123'
        create_admin_user(username, email, password)
    else:
        create_admin_user()
    
    print("\nDone!") 