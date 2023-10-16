#!/bin/sh

# Apply database migrations
python manage.py migrate

# Start server
exec "$@"
