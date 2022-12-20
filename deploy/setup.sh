#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/BasinaLikithViswanath/taskApi'
PROJECT_BASE_PATH='/usr/local/apps/taskApi'

# Set Ubuntu Language
locale-gen en_GB.UTF-8

# Install Python, SQLite and pip
#echo "Installing dependencies..."
#apt-get update
#apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Create project directory
#mkdir -p $PROJECT_BASE_PATH
#git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
#mkdir -p $PROJECT_BASE_PATH/env
#python3 -m venv $PROJECT_BASE_PATH/env

#install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
#$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.20

# run migrations
#cd $PROJECT_BASE_PATH
#$PROJECT_BASE_PATH/env/bin/python manage.py migrate
#$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Setup Supervisor to run our uwsgi process.
#cp $PROJECT_BASE_PATH/deploy/supervisor_taskApi.conf /etc/supervisor/conf.d/taskApi.conf
#supervisorctl reread
#supervisorctl update
#supervisorctl restart taskApi

# Setup nginx to make our application accessible.
#cp $PROJECT_BASE_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/taskApi.conf
#rm /etc/nginx/sites-enabled/default
#ln -s /etc/nginx/sites-available/taskApi.conf /etc/nginx/sites-enabled/taskApi.conf
#systemctl restart nginx.service

echo "DONE! :)"
