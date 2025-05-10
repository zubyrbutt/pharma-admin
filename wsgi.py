import os
import sys
from flask_migrate import upgrade
from app import create_app, db
from app.models.user import User

# Use FLASK_ENV if set, otherwise use 'production'
env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)

# For compatibility with common WSGI servers like Gunicorn
application = app  # This is for WSGI servers that look for 'application'

# Initialize database when running on Render
if os.getenv('RENDER'):
    with app.app_context():
        try:
            # Run migrations
            upgrade()
            
            # Add admin user if doesn't exist
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                admin = User(
                    email='admin@example.com',
                    username='admin',
                    admin=True
                )
                admin.password = 'adminpassword'  # Will be hashed by the model
                db.session.add(admin)
                db.session.commit()
                print("Created admin user: admin@example.com with password: adminpassword")
        except Exception as e:
            print(f"Error initializing database: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000))) 