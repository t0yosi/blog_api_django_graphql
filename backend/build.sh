#!/bin/bash

# Step 1: Navigate to your project directory
cd /path/to/your/project

# Step 2: Set up a virtual environment (if not already set up)
echo "Setting up a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 3: Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Step 5: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput