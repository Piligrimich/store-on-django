#!/bin/sh

# python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

exec "$@"
