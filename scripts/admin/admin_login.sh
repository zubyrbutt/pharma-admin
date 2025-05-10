#!/bin/bash
# Admin login shell script using curl

# Configuration
BASE_URL="http://localhost:5050"
ADMIN_EMAIL=${ADMIN_EMAIL:-"admin@example.com"}
ADMIN_PASSWORD=${ADMIN_PASSWORD:-"admin123"}
COOKIE_JAR="admin_cookies.txt"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=== Admin Login Shell Script ==="
echo "BASE URL: $BASE_URL"
echo "ADMIN EMAIL: $ADMIN_EMAIL"
echo "ADMIN PASSWORD: ${ADMIN_PASSWORD//?/*}"
echo ""

# Remove cookie jar if exists
rm -f "$COOKIE_JAR"

# Step 1: Get CSRF token (if needed)
echo "1. Checking home page redirect..."
RESPONSE=$(curl -s -L -c "$COOKIE_JAR" "$BASE_URL/")
if [[ "$RESPONSE" == *"Admin Login"* ]]; then
    echo -e "${GREEN}✓ Successfully accessed login page${NC}"
else
    echo -e "${RED}✗ Failed to access login page${NC}"
    exit 1
fi

# Step 2: Log in
echo -e "\n2. Logging in with admin credentials..."
RESPONSE=$(curl -s -L -b "$COOKIE_JAR" -c "$COOKIE_JAR" \
    -d "email=$ADMIN_EMAIL" \
    -d "password=$ADMIN_PASSWORD" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "$BASE_URL/admin/login")

if [[ "$RESPONSE" == *"Admin Dashboard"* ]]; then
    echo -e "${GREEN}✓ Login successful!${NC}"
else
    echo -e "${RED}✗ Login failed!${NC}"
    # Check for error message
    if [[ "$RESPONSE" == *"Invalid email or password"* ]]; then
        echo "Error: Invalid email or password"
    fi
    exit 1
fi

# Step 3: Access dashboard
echo -e "\n3. Accessing dashboard to verify login state..."
RESPONSE=$(curl -s -L -b "$COOKIE_JAR" "$BASE_URL/admin/dashboard")

if [[ "$RESPONSE" == *"Admin Dashboard"* ]]; then
    echo -e "${GREEN}✓ Successfully accessed dashboard!${NC}"
    
    # For macOS compatibility, simpler detection without extracting numbers
    if [[ "$RESPONSE" == *"<h2>"*"</h2>"*"<p>Users</p>"* ]]; then
        echo -e "${GREEN}✓ Found Users statistic${NC}"
    fi
    
    if [[ "$RESPONSE" == *"<h2>"*"</h2>"*"<p>Items</p>"* ]]; then
        echo -e "${GREEN}✓ Found Items statistic${NC}"
    fi
    
    if [[ "$RESPONSE" == *"<h2>"*"</h2>"*"<p>Active Users</p>"* ]]; then
        echo -e "${GREEN}✓ Found Active Users statistic${NC}"
    fi
else
    echo -e "${RED}✗ Failed to access dashboard!${NC}"
    exit 1
fi

# Step 4: Log out
echo -e "\n4. Logging out..."
RESPONSE=$(curl -s -L -b "$COOKIE_JAR" "$BASE_URL/admin/logout")

if [[ "$RESPONSE" == *"Admin Login"* ]]; then
    echo -e "${GREEN}✓ Successfully logged out!${NC}"
else
    echo -e "${RED}✗ Logout failed!${NC}"
    exit 1
fi

# Clean up
rm -f "$COOKIE_JAR"
echo -e "\n${GREEN}✓ Admin login flow completed successfully!${NC}" 