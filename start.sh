#!/bin/bash

# check Mariadb availability
while ! mysqladmin ping -h"$DB_HOST" --silent; do
    echo "wait for database"
    sleep 5
done

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo "Successful migrate database"

# Update data
echo "Update matches"
python manage.py fetch_and_update_match
echo "Update players"
python manage.py update_player
echo "Generate Score Table"
python manage.py generate_score_table

# Start server
gunicorn --env DJANGO_SETTINGS_MODULE=projectviolet.settings_prod -b 0.0.0.0:8000 projectviolet.wsgi --workers 1
