import os
import json
from flask import Flask, jsonify, send_from_directory, render_template, request, redirect, url_for, session, flash
from flask_restful import Api
from werkzeug.security import check_password_hash
from functools import wraps

from app import create_app, db
from app.models.user import User
from app.models.item import Item
from app.models.pharmaceutical import Company, Drug, Brand, AdultDosage, PediatricDosage, NeonatalDosage

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'default'))

# Admin login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin', False):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Load JSON data function
def load_json_data(file_path, limit=None):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data[:limit] if limit else data
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []

# Routes
@app.route('/')
def home():
    """Home route that redirects to dashboard if logged in, otherwise to login page"""
    if 'user_id' in session and session.get('is_admin', False):
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/api')
def api_info():
    """API info endpoint that returns JSON information."""
    return {
        "message": "Welcome to the Advanced Flask API",
        "version": "1.0",
        "documentation": "/api/docs",
        "endpoints": {
            "users": "/api/v1/users",
            "items": "/api/v1/items",
            "login": "/api/v1/login"
        }
    }

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if 'user_id' in session and session.get('is_admin', False):
        return redirect(url_for('admin_dashboard'))
    
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.admin and user.verify_password(password):
            session['user_id'] = user.id
            session['is_admin'] = user.admin
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid email or password, or not an admin user.'
    
    return render_template('admin/login.html', error=error)

@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    """Admin dashboard with pharmaceutical data."""
    # Get current user
    user = User.query.get(session['user_id'])
    
    # Get stats
    user_count = User.query.count()
    item_count = Item.query.count()
    active_users = User.query.filter_by(active=True).count()
    
    # Get pharmaceutical data from database
    companies = Company.query.all()
    brands = Brand.query.all()
    adult_dosages = AdultDosage.query.all()
    pediatric_dosages = PediatricDosage.query.all()
    neonatal_dosages = NeonatalDosage.query.all()
    
    # Count total records
    company_count = Company.query.count()
    brand_count = Brand.query.count()
    
    # Get all users and items
    users = User.query.all()
    items = Item.query.all()
    
    return render_template('admin/dashboard.html', 
                           user=user,
                           user_count=user_count,
                           item_count=item_count, 
                           active_users=active_users,
                           users=users,
                           items=items,
                           companies=companies,
                           brands=brands,
                           adult_dosages=adult_dosages,
                           pediatric_dosages=pediatric_dosages,
                           neonatal_dosages=neonatal_dosages,
                           company_count=company_count,
                           brand_count=brand_count)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

# CRUD routes for users and items in the admin panel
@app.route('/admin/users/add', methods=['GET', 'POST'])
@admin_login_required
def admin_add_user():
    """Add a new user from admin panel."""
    # This is a placeholder - you'd implement a form to add a user
    return "Admin Add User Page - Not Implemented"

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_user(user_id):
    """Edit a user from admin panel."""
    # This is a placeholder - you'd implement a form to edit a user
    return f"Admin Edit User Page for User ID: {user_id} - Not Implemented"

@app.route('/admin/users/delete/<int:user_id>')
@admin_login_required
def admin_delete_user(user_id):
    """Delete a user from admin panel."""
    # This is a placeholder - you'd implement deletion logic
    return f"Admin Delete User for User ID: {user_id} - Not Implemented"

@app.route('/admin/items/add', methods=['GET', 'POST'])
@admin_login_required
def admin_add_item():
    """Add a new item from admin panel."""
    # This is a placeholder - you'd implement a form to add an item
    return "Admin Add Item Page - Not Implemented"

@app.route('/admin/items/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_item(item_id):
    """Edit an item from admin panel."""
    # This is a placeholder - you'd implement a form to edit an item
    return f"Admin Edit Item Page for Item ID: {item_id} - Not Implemented"

@app.route('/admin/items/delete/<int:item_id>')
@admin_login_required
def admin_delete_item(item_id):
    """Delete an item from admin panel."""
    # This is a placeholder - you'd implement deletion logic
    return f"Admin Delete Item for Item ID: {item_id} - Not Implemented"

if __name__ == '__main__':
    # No need to register blueprints here as they're registered in create_app
    
    # Run the app on port 5050 to avoid conflicts
    app.run(host='0.0.0.0', debug=True, port=5050) 