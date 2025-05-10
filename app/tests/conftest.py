import os
import pytest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models.user import User
from app.models.item import Item


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
        
        # Create test user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='password',
            admin=True
        )
        
        regular_user = User(
            username='user',
            email='user@example.com',
            password='password'
        )
        
        db.session.add(admin_user)
        db.session.add(regular_user)
        db.session.commit()
        
        # Create test items
        item1 = Item(
            name='Test Item 1',
            description='Description for test item 1',
            price=10.99,
            quantity=5,
            user_id=regular_user.id
        )
        
        item2 = Item(
            name='Test Item 2',
            description='Description for test item 2',
            price=20.49,
            quantity=10,
            user_id=admin_user.id
        )
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.commit()
    
    yield app
    
    # Clean up / reset resources
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def admin_user_id(app):
    """Get the ID of the admin user."""
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        return admin.id


@pytest.fixture
def regular_user_id(app):
    """Get the ID of the regular user."""
    with app.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        return user.id


@pytest.fixture
def admin_headers(app, admin_user_id):
    """Create headers with admin user JWT token."""
    with app.app_context():
        access_token = create_access_token(identity=admin_user_id)
        return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def user_headers(app, regular_user_id):
    """Create headers with regular user JWT token."""
    with app.app_context():
        access_token = create_access_token(identity=regular_user_id)
        return {'Authorization': f'Bearer {access_token}'} 