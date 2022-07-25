#!/usr/bin/env sh

set -e

echo "entrypoint"

#. ./django-entrypoint.sh
. ./celery-entrypoint.sh
