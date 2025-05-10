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
- Testing infrastructure

## Setup

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

## API Documentation

API endpoints are available at `/api/v1/...`

## Testing

```bash
pytest
``` 