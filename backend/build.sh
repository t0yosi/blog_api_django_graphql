#!/bin/bash

# Step 1: Update and install dependencies
echo "Updating system and installing dependencies..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-dev libpq-dev nginx

# Step 2: Navigate to your project directory
cd /path/to/your/project

# Step 3: Set up a virtual environment
echo "Setting up a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 4: Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# LOG DIRECTORY
mkdir -p /opt/render/project/src/backend/logs 

# Step 5: Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Step 6: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 7: Start the Django development server (for testing purposes)
echo "Starting the Django development server..."
python manage.py runserver 0.0.0.0:8000

# Uncomment the lines below if deploying to production with Gunicorn and Nginx

# Step 8: Install and configure Gunicorn
# echo "Installing and configuring Gunicorn..."
# pip install gunicorn
# gunicorn --bind 0.0.0.0:8000 your_project_name.wsgi:application

# Step 9: Set up Nginx to proxy pass to Gunicorn
# echo "Configuring Nginx..."
# sudo cp /path/to/your/project/nginx_config /etc/nginx/sites-available/your_project_name
# sudo ln -s /etc/nginx/sites-available/your_project_name /etc/nginx/sites-enabled
# sudo nginx -t
# sudo systemctl restart nginx

echo "Deployment complete! Your app is running at http://your-server-ip:8000"
