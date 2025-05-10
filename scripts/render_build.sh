#!/bin/bash
# This script runs during the build process on Render

# Set environment variable to identify we're on Render
export RENDER=true

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Initialize database if needed
echo "Initializing database with seed data..."
python scripts/init_db.py

echo "Build process completed successfully." 