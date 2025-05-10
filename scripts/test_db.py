import os
import sys

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User

def test_db_connection():
    """Test database connectivity and query a user."""
    app = create_app(os.getenv('FLASK_ENV', 'production'))
    
    with app.app_context():
        try:
            # Try to query the database
            users = User.query.all()
            print(f"Database connection successful! Found {len(users)} users.")
            
            # Print info about each user
            for user in users:
                print(f"User: {user.username}, Email: {user.email}, Admin: {user.admin}")
                
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

if __name__ == '__main__':
    test_db_connection() 