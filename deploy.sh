#!/bin/bash

set -e  # Para si hay algún error

git pull origin main
docker compose down
docker compose up --build -d
docker compose exec backend uv run manage.py migrate --noinput
docker compose exec backend uv run manage.py collectstatic --noinput
cp backend/db.sqlite3 backend/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
echo "Despliegue completado"
