import json
import pytest
from app.models.item import Item
from app.models.user import User


def test_create_item(client, user_headers):
    """Test creating a new item."""
    response = client.post('/api/v1/items', headers=user_headers, json={
        'name': 'New Test Item',
        'description': 'This is a test item',
        'price': 15.99,
        'quantity': 3
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New Test Item'
    assert data['price'] == 15.99
    assert data['quantity'] == 3


def test_get_items_list(client, user_headers):
    """Test getting items list."""
    response = client.get('/api/v1/items', headers=user_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Regular user should only see their own items
    user = User.query.filter_by(email='user@example.com').first()
    for item in data:
        assert item['user_id'] == user.id


def test_get_items_list_as_admin(client, admin_headers):
    """Test getting items list as admin (should see all items)."""
    response = client.get('/api/v1/items', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2  # At least the two items from fixtures


def test_get_item_detail(client, user_headers):
    """Test getting item detail."""
    # First get the user's item ID
    user = User.query.filter_by(email='user@example.com').first()
    item = Item.query.filter_by(user_id=user.id).first()
    
    response = client.get(f'/api/v1/items/{item.id}', headers=user_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == item.id
    assert data['name'] == item.name


def test_get_other_user_item_detail(client, user_headers):
    """Test getting another user's item detail (should fail)."""
    # Get an admin user's item ID
    admin = User.query.filter_by(email='admin@example.com').first()
    item = Item.query.filter_by(user_id=admin.id).first()
    
    response = client.get(f'/api/v1/items/{item.id}', headers=user_headers)
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_update_item(client, user_headers):
    """Test updating an item."""
    # First get the user's item ID
    user = User.query.filter_by(email='user@example.com').first()
    item = Item.query.filter_by(user_id=user.id).first()
    
    response = client.put(f'/api/v1/items/{item.id}', headers=user_headers, json={
        'name': 'Updated Item Name',
        'price': 25.99
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated Item Name'
    assert data['price'] == 25.99
    # Check that other fields were not changed
    assert data['description'] == item.description
    assert data['quantity'] == item.quantity


def test_delete_item(client, user_headers):
    """Test deleting an item."""
    # First create a new item to delete
    create_response = client.post('/api/v1/items', headers=user_headers, json={
        'name': 'Item to Delete',
        'description': 'This item will be deleted',
        'price': 9.99,
        'quantity': 1
    })
    
    create_data = json.loads(create_response.data)
    item_id = create_data['id']
    
    # Now delete it
    delete_response = client.delete(f'/api/v1/items/{item_id}', headers=user_headers)
    
    assert delete_response.status_code == 200
    delete_data = json.loads(delete_response.data)
    assert 'deleted successfully' in delete_data['message']
    
    # Verify it's gone
    get_response = client.get(f'/api/v1/items/{item_id}', headers=user_headers)
    assert get_response.status_code == 404 