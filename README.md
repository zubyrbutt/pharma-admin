# Advanced Flask Application

A modern Flask application with RESTful API, SQLAlchemy ORM, JWT authentication, and more.

## Features

- RESTful API architecture
- SQLAlchemy ORM for database interactions
- JWT authentication and authorization
- Environment-based configuration
- Blueprint-based modular structure
- Database migrations with Flask-Migrate
- Error handling and logging
- Admin dashboard and login system
- Testing infrastructure

## Setup

### Quick Setup

For a quick setup that handles everything automatically:

```bash
# Run the setup script
./setup.sh
```

This script will:
1. Create and activate a virtual environment
2. Install dependencies
3. Initialize the database
4. Create an admin user
5. Offer to start the application

### Manual Setup

### Install dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///app.db
```

### Initialize the database

```bash
# Initialize database with tables and admin user
python scripts/init_database.py

# Alternatively, use Flask-Migrate for schema migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Run the application

```bash
flask run
```

For production:

```bash
gunicorn wsgi:app
```

## Admin Interface

The application includes an admin interface:

- Access the admin panel at `/admin/login`
- Default admin credentials: admin@example.com / admin123

### Admin Scripts

The `scripts/admin/` directory contains utilities for working with the admin interface:

```bash
# Create or update admin users
python scripts/admin/create_admin.py

# Test admin login flow
python scripts/admin/admin_login_script.py

# Programmatic API access
python scripts/admin/admin_api.py
```

See `scripts/admin/README.md` for detailed documentation on admin scripts.

## API Documentation

API endpoints are available at `/api/v1/...`

## Testing

```bash
pytest
``` 