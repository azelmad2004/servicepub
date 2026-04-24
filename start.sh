#!/bin/bash

echo "Running migrations..."
python manage.py migrate

echo "Seeding database..."
python seed_users.py
python seed_services.py

echo "Starting server..."
gunicorn servicepub.wsgi --log-file -
