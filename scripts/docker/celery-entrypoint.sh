#!/usr/bin/env sh
echo "celery-entrypoint"


poetry run celery -A brew_notifier worker -l INFO -Q reqular,high-priority