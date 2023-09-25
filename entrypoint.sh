#!/bin/bash
python manage.py migrate

python manage.py collectstatic --clear --noinput

cp -r /app/static/. /backend_static/static/

gunicorn meeco.wsgi:application --bind 0.0.0.0:8000
