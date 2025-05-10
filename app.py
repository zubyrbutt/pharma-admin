import os
from app import create_app

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    # Run the app on port 5050 to avoid conflicts
    app.run(host='0.0.0.0', debug=True, port=5050) 