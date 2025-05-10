import os
from app import create_app

# Use FLASK_ENV if set, otherwise use 'production'
env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)

# Create the Flask application instance
application = app

# For compatibility with common WSGI servers like Gunicorn
app = application

if __name__ == "__main__":
    app.run() 