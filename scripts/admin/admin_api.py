#!/usr/bin/env python3
"""
Admin API helper script for programmatic access
This can be imported and used in other scripts or run directly
"""

import os
import sys
import json
import requests
from requests.exceptions import RequestException

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class AdminAPI:
    def __init__(self, base_url=None, admin_email=None, admin_password=None):
        """Initialize with optional credentials from args or environment vars"""
        self.base_url = base_url or os.environ.get('API_BASE_URL', 'http://localhost:5050')
        self.admin_email = admin_email or os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        self.admin_password = admin_password or os.environ.get('ADMIN_PASSWORD', 'admin123')
        self.session = requests.Session()
        self.logged_in = False
    
    def login(self):
        """Log in to the admin interface"""
        try:
            login_data = {
                'email': self.admin_email,
                'password': self.admin_password
            }
            
            response = self.session.post(f"{self.base_url}/admin/login", data=login_data)
            
            # Check if login succeeded (should redirect to dashboard)
            if response.url.endswith('/admin/dashboard'):
                self.logged_in = True
                return True, "Login successful"
            else:
                return False, f"Login failed: {response.url}"
                
        except RequestException as e:
            return False, f"Error connecting to server: {str(e)}"
    
    def logout(self):
        """Log out from the admin interface"""
        try:
            response = self.session.get(f"{self.base_url}/admin/logout")
            if response.url.endswith('/admin/login'):
                self.logged_in = False
                return True, "Logout successful"
            else:
                return False, f"Logout failed: {response.url}"
        except RequestException as e:
            return False, f"Error during logout: {str(e)}"
    
    def get_dashboard_data(self):
        """Extract data from the dashboard"""
        if not self.logged_in:
            success, message = self.login()
            if not success:
                return False, message
        
        try:
            response = self.session.get(f"{self.base_url}/admin/dashboard")
            
            if response.status_code != 200:
                return False, f"Failed to access dashboard: {response.status_code}"
            
            # Very basic HTML parsing to extract stats
            # In a real application, you might want to use BeautifulSoup
            import re
            
            stats = {}
            
            # Extract user count
            user_match = re.search(r'<h2>(\d+)</h2>\s*<p>Users</p>', response.text)
            if user_match:
                stats['user_count'] = int(user_match.group(1))
            
            # Extract item count
            item_match = re.search(r'<h2>(\d+)</h2>\s*<p>Items</p>', response.text)
            if item_match:
                stats['item_count'] = int(item_match.group(1))
            
            # Extract active users
            active_match = re.search(r'<h2>(\d+)</h2>\s*<p>Active Users</p>', response.text)
            if active_match:
                stats['active_users'] = int(active_match.group(1))
            
            return True, stats
            
        except RequestException as e:
            return False, f"Error accessing dashboard: {str(e)}"
    
    def run_demo(self):
        """Run a demo of all API features"""
        print(f"=== Admin API Demo ===")
        print(f"Base URL: {self.base_url}")
        print(f"Admin Email: {self.admin_email}")
        print(f"Admin Password: {'*' * len(self.admin_password)}")
        
        print("\n1. Logging in...")
        success, message = self.login()
        print(f"{'✓' if success else '✗'} {message}")
        
        if success:
            print("\n2. Getting dashboard data...")
            success, data = self.get_dashboard_data()
            if success:
                print("✓ Successfully retrieved dashboard data:")
                for key, value in data.items():
                    print(f"  - {key}: {value}")
            else:
                print(f"✗ {data}")
            
            print("\n3. Logging out...")
            success, message = self.logout()
            print(f"{'✓' if success else '✗'} {message}")
        
        print("\nDemo completed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Admin API Helper')
    parser.add_argument('--url', help='Base URL of the API')
    parser.add_argument('--email', help='Admin email')
    parser.add_argument('--password', help='Admin password')
    args = parser.parse_args()
    
    api = AdminAPI(
        base_url=args.url,
        admin_email=args.email,
        admin_password=args.password
    )
    
    api.run_demo() 