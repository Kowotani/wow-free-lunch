#!/bin/sh

until cd /app/backend/server
do
    echo 'Waiting for server volume...'
    sleep 2
done

until cd /app/backend/dj_wfl
do
    echo 'Waiting for Django volume...'
    sleep 2
done

python /app/backend/dj_wfl/manage.py collectstatic --noinput

gunicorn dj_wfl.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# Options to DEBUG Django server
# Optional commands to replace above gunicorn command

# Option 1:
# run gunicorn with debug log level
# gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 1 --threads 1 --log-level debug

# Option 2:
# run development server
# python manage.py runserver 0.0.0.0:8000