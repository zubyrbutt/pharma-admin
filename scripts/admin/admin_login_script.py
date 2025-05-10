#!/usr/bin/env python3
import os
import sys
import requests
from flask import session

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def login_via_api():
    """Login to admin interface via direct API call"""
    base_url = "http://localhost:5050"
    
    print("Attempting to login via direct API call...")
    
    # Admin credentials
    admin_data = {
        'email': 'admin@example.com',  # Replace with your admin email
        'password': 'admin123'         # Replace with your admin password
    }
    
    # Create a session to maintain cookies
    s = requests.Session()
    
    # First check redirect from home
    print("1. Checking redirect from homepage...")
    response = s.get(f"{base_url}/")
    if response.url.endswith('/admin/login'):
        print(f"✓ Successfully redirected to login page: {response.url}")
    else:
        print(f"✗ Unexpected redirect to: {response.url}")
    
    # Login to admin panel
    print("\n2. Attempting login with admin credentials...")
    login_response = s.post(f"{base_url}/admin/login", data=admin_data)
    
    # Check if login succeeded (should redirect to dashboard)
    if login_response.url.endswith('/admin/dashboard'):
        print(f"✓ Login successful! Redirected to: {login_response.url}")
        print(f"✓ Status code: {login_response.status_code}")
    else:
        print(f"✗ Login failed. Current page: {login_response.url}")
        print(f"✗ Status code: {login_response.status_code}")
        if 'error' in login_response.text:
            print("Error message found on page. Login credentials may be incorrect.")
        return False
    
    # Try accessing protected route
    print("\n3. Accessing dashboard to verify login state...")
    dashboard = s.get(f"{base_url}/admin/dashboard")
    if dashboard.status_code == 200:
        print("✓ Successfully accessed dashboard!")
        
        # Extract some stats from the page as proof
        if "Admin Dashboard" in dashboard.text:
            print("✓ Confirmed page contains 'Admin Dashboard' title")
        
        # Try to extract user count from stats (simple approach)
        import re
        users_match = re.search(r'<h2>(\d+)</h2>\s*<p>Users</p>', dashboard.text)
        if users_match:
            print(f"✓ Found user count: {users_match.group(1)}")
    else:
        print(f"✗ Failed to access dashboard. Status code: {dashboard.status_code}")
        return False
    
    # Try logout
    print("\n4. Testing logout functionality...")
    logout = s.get(f"{base_url}/admin/logout")
    if logout.url.endswith('/admin/login'):
        print("✓ Successfully logged out!")
    else:
        print(f"✗ Logout may have failed. Current page: {logout.url}")
    
    return True

def create_admin_with_flask_shell():
    """Print instructions for creating an admin user with Flask shell"""
    print("\n=== How to create an admin user with Flask shell ===")
    print("Run these commands in a Python shell within your Flask application context:")
    print("\nfrom app import app, db")
    print("from app.models.user import User")
    print("with app.app_context():")
    print("    # Check if admin exists")
    print("    admin = User.query.filter_by(email='admin@example.com').first()")
    print("    if not admin:")
    print("        admin = User(username='admin', email='admin@example.com', active=True, admin=True)")
    print("        admin.password = 'admin123'  # Will be automatically hashed")
    print("        db.session.add(admin)")
    print("        db.session.commit()")
    print("        print('Admin user created!')")
    print("    else:")
    print("        print('Admin user already exists')")

if __name__ == "__main__":
    print("=== Admin Login Script ===\n")
    
    if not login_via_api():
        print("\n✗ Login process failed.")
        print("This could be because:")
        print("1. The Flask app is not running on localhost:5050")
        print("2. Admin credentials are incorrect")
        print("3. Admin user doesn't exist in the database")
        
        create_admin_with_flask_shell()
    else:
        print("\n✓ Admin login flow completed successfully!") 