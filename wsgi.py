import os
from app import create_app

# Use FLASK_ENV if set, otherwise use 'production'
env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)

# For compatibility with common WSGI servers like Gunicorn
application = app  # This is for WSGI servers that look for 'application'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000))) 