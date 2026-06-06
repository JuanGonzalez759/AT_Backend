#!/usr/bin/env bash
set -euo pipefail

# Change to project root (AT_Backend) so manage.py is reachable
cd "$(dirname "$0")/.."

echo "--- STARTUP DEBUG ---"
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Environment variables (filtered):"
echo "  DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-not-set}"
echo "  CLOUDINARY_URL=${CLOUDINARY_URL:+set}"
echo "  RENDER_ADMIN_USER=${RENDER_ADMIN_USER:-not-set}"
echo "  RENDER_ADMIN_PASS=${RENDER_ADMIN_PASS:+set}"
echo "  RENDER_ADMIN_EMAIL=${RENDER_ADMIN_EMAIL:-not-set}"
echo "  PORT=${PORT:-not-set}"

echo "--- DJANGO SETTINGS ---"
python - <<PY
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
django.setup()
from django.conf import settings
print('DEBUG=', getattr(settings,'DEBUG',None))
print('ALLOWED_HOSTS=', getattr(settings,'ALLOWED_HOSTS',None))
print('DEFAULT_FILE_STORAGE=', getattr(settings,'DEFAULT_FILE_STORAGE',None))
print('MEDIA_ROOT=', getattr(settings,'MEDIA_ROOT',None))
print('STATIC_ROOT=', getattr(settings,'STATIC_ROOT',None))
PY

echo "--- RUNNING django check ---"
python manage.py check || true

echo "--- STARTING GUNICORN ---"
exec gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --log-file -
