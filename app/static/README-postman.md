# Pharma API Postman Collection

This folder contains a Postman collection for testing the Pharma API.

## Getting Started

### Prerequisites

1. [Postman](https://www.postman.com/downloads/) installed on your computer
2. The Pharma API running locally or on a server

### Importing the Collection

1. Open Postman
2. Click on "Import" in the top left corner
3. Select "File" and browse to `app/static/pharma-api-postman-collection.json`
4. Click "Import"

### Setting Up Environment Variables

The collection uses two variables that you need to configure:

1. `baseUrl` - The base URL of the API (default: `http://localhost:5050`)
2. `accessToken` - Your JWT authentication token (obtained after login)

To set these up:

1. In Postman, click on "Environments" in the left sidebar
2. Click "+" to create a new environment
3. Name it "Pharma API Environment"
4. Add the following variables:
   - `baseUrl`: `http://localhost:5050` (or your actual API URL)
   - `accessToken`: Leave this empty for now
5. Click "Save"
6. Select the environment from the dropdown in the top right corner

### Authentication

To authenticate and get your access token:

1. Navigate to the "Authentication" folder in the collection
2. Open the "Login to get access token" request
3. Update the request body with your credentials
4. Send the request
5. In the response, find the "access_token" value
6. Copy this token and set it as the value for the `accessToken` environment variable

### Using the Collection

The collection is organized into folders by resource type:

- **Authentication** - Login endpoint
- **Users** - User management operations
- **Items** - Item management operations
- **Companies** - Pharmaceutical company operations
- **Drugs** - Drug information operations
- **Brands** - Brand management operations
- **Dosages** - Dosage information operations (Adult, Pediatric, Neonatal)

Each folder contains requests for common operations (GET, POST, PUT, DELETE) on that resource.

## Tips

- For admin-only endpoints, make sure you're logged in with an admin account
- Most creation (POST) and update (PUT) requests have example request bodies that you can modify
- You can use the "GET all" requests to view existing resources and their IDs
- Remember to update the IDs in URL paths for specific resource operations 