#!/bin/bash
python manage.py migrate

python manage.py collectstatic --clear --noinput

cp -r /app/collected_static/. /backend_static/static/

gunicorn meecco.wsgi:application --bind 0.0.0.0:8000
