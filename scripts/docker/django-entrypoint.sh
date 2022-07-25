#!/usr/bin/env sh
echo "django-entrypoint"

poetry run python manage.py collectstatic --no-input

poetry run gunicorn brew_notifier.wsgi:application --bind 0.0.0.0:8000