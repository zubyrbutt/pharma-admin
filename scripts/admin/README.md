# Admin Scripts

This directory contains scripts to manage admin tasks for the Flask API application.

## First Time Setup: Initialize the Database

Before using any admin scripts, you must initialize the database:

```bash
# Initialize the database and create admin user
python scripts/init_database.py

# Optional: Use custom admin credentials
python scripts/init_database.py --username admin --email admin@example.com --password strongpassword
```

This script:
1. Creates all database tables
2. Creates an initial admin user
3. Displays database summary information

## Setting Up an Admin User

After initializing the database, you can create additional admin users or reset passwords:

```bash
# Run the admin user creation script
python scripts/admin/create_admin.py
```

The script will:
1. Create a new admin user with default credentials if one doesn't exist
2. Offer to reset the password for an existing admin
3. Allow you to customize the admin credentials

Default credentials:
- Username: admin
- Email: admin@example.com
- Password: admin123

## Admin Login Scripts

### Python Script

The Python login script demonstrates how to log in programmatically:

```bash
# Run the automated login script
python scripts/admin/admin_login_script.py
```

This script:
1. Attempts to log in with admin credentials
2. Accesses the dashboard to verify login state
3. Extracts information from the dashboard
4. Logs out

### Shell Script (Curl)

For command-line usage, there's a shell script using curl:

```bash
# Run the shell script
./scripts/admin/admin_login.sh
```

You can customize credentials with environment variables:

```bash
ADMIN_EMAIL="custom@example.com" ADMIN_PASSWORD="mysecret" ./scripts/admin/admin_login.sh
```

### Admin API Class

For more advanced usage, use the AdminAPI class:

```bash
# Run the API demo
python scripts/admin/admin_api.py

# Use with custom parameters
python scripts/admin/admin_api.py --url http://example.com:5050 --email admin@example.com --password secretpassword
```

You can also import this class in other Python scripts:

```python
from scripts.admin.admin_api import AdminAPI

# Create API instance
api = AdminAPI()

# Login
success, message = api.login()
if success:
    # Get dashboard data
    success, data = api.get_dashboard_data()
    if success:
        print(f"User count: {data.get('user_count')}")
        print(f"Item count: {data.get('item_count')}")
    
    # Logout
    api.logout()
```

## Environment Variables

All scripts support customization through environment variables:

- `API_BASE_URL` - Base URL of the API (default: http://localhost:5050)
- `ADMIN_EMAIL` - Admin email address (default: admin@example.com)
- `ADMIN_PASSWORD` - Admin password (default: admin123)

## Troubleshooting

### No such table: users

If you get an error like `sqlite3.OperationalError: no such table: users`, it means you need to initialize the database first:

```bash
python scripts/init_database.py
```

This will create all the necessary database tables before attempting to create users. 