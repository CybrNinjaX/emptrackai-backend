#!/usr/bin/env sh
set -eu

# runserver applies saved Django migrations before starting.
exec python manage.py runserver "0.0.0.0:${PORT:-8000}"
