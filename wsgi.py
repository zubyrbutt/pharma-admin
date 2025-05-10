import os
from app import create_app

# Use FLASK_ENV if set, otherwise use 'production'
env = os.getenv('FLASK_ENV', 'production')
app = create_app(env) 