#!/bin/sh
set -euo pipefail

cd /backend

echo "Running database migrations..."
alembic upgrade head

echo "Seeding database with sample data (if empty)..."
python -m db.seed

echo "Starting application..."
exec python -m app
