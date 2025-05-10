import json
import pytest
from app.models.user import User


def test_user_registration(client):
    """Test user registration."""
    response = client.post('/api/v1/users', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'
    assert 'password' not in data


def test_user_login(client):
    """Test user login."""
    # Register a new user first
    client.post('/api/v1/users', json={
        'username': 'logintest',
        'email': 'logintest@example.com',
        'password': 'password123'
    })
    
    # Try to login
    response = client.post('/api/v1/login', json={
        'email': 'logintest@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Login successful'
    assert 'access_token' in data
    assert 'user' in data


def test_get_users_list_as_admin(client, admin_headers):
    """Test getting users list as admin."""
    response = client.get('/api/v1/users', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2  # At least the admin and regular user from fixtures


def test_get_users_list_as_user(client, user_headers):
    """Test getting users list as regular user (should fail)."""
    response = client.get('/api/v1/users', headers=user_headers)
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_get_user_profile(client, user_headers):
    """Test getting own user profile."""
    # First get the user ID
    user = User.query.filter_by(email='user@example.com').first()
    
    response = client.get(f'/api/v1/users/{user.id}', headers=user_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'user@example.com'


def test_get_other_user_profile_as_user(client, user_headers):
    """Test getting another user's profile as regular user (should fail)."""
    # Get the admin user ID
    admin = User.query.filter_by(email='admin@example.com').first()
    
    response = client.get(f'/api/v1/users/{admin.id}', headers=user_headers)
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_update_user_profile(client, user_headers):
    """Test updating own user profile."""
    # First get the user ID
    user = User.query.filter_by(email='user@example.com').first()
    
    response = client.put(f'/api/v1/users/{user.id}', headers=user_headers, json={
        'username': 'updated_username'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'updated_username'
    assert data['email'] == 'user@example.com' 