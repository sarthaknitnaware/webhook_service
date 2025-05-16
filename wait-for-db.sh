#!/bin/sh

# Wait until PostgreSQL is ready
echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL is up. Starting app..."

# Run the FastAPI app
exec "$@"

