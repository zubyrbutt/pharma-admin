#!/bin/bash
# Setup script for initializing and running the Flask application

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Flask API Application Setup ===${NC}"

# Check for Python
echo -e "\n${YELLOW}Checking for Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is required but not found. Please install Python 3.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"

# Set up virtual environment
echo -e "\n${YELLOW}Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
python scripts/init_database.py
echo -e "${GREEN}✓ Database initialized${NC}"

# Run the application
echo -e "\n${YELLOW}Starting Flask application...${NC}"
echo -e "${GREEN}✓ Application can now be started with: python app.py${NC}"
echo -e "${GREEN}✓ Or for development: FLASK_APP=app.py FLASK_ENV=development flask run${NC}"
echo -e "${GREEN}✓ Admin login: http://localhost:5050/admin/login${NC}"
echo -e "${GREEN}✓ Default credentials: admin@example.com / admin123${NC}"

# Offer to run the application
echo -e "\n${YELLOW}Would you like to run the application now? (y/n)${NC}"
read -r RUN_APP
if [[ $RUN_APP =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Starting application on http://localhost:5050...${NC}"
    python app.py
fi 