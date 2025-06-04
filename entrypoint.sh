#!/bin/bash

export PYTHONPATH="/app:$PYTHONPATH"

# Aplica migrações do banco de dados
echo "Applying database migrations..."
python manage.py migrate --noinput || { echo "Database migrations failed!" && exit 1; }

# Inicia o servidor Gunicorn
echo "Starting Gunicorn server..."

exec gunicorn Core.wsgi:application --bind 0.0.0.0:8000 --workers 3
