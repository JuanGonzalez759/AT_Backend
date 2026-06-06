#!/usr/bin/env bash
set -euo pipefail

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

echo "=== BUILD DIAGNOSTIC: PWD ==="
pwd
echo "=== BUILD DIAGNOSTIC: LISTING CURRENT DIR ==="
ls -la
echo "=== BUILD DIAGNOSTIC: LISTING PARENT DIR ==="
ls -la ..
echo "=== BUILD DIAGNOSTIC: TRY HEAD fixtures.json ==="
head -n 20 fixtures.json || true
echo "=== BUILD DIAGNOSTIC: TRY HEAD AT_Backend/fixtures.json ==="
head -n 20 AT_Backend/fixtures.json || true

# Normalize JSON fixtures to remove UTF-8 BOM if present (prevents JSONDecodeError in loaddata)
# Use Python's utf-8-sig codec to safely remove BOM if present and rewrite file
for f in fixtures.json AT_Backend/fixtures.json; do
  if [ -f "$f" ]; then
    echo "Normalizing JSON encoding for $f"
    python - "$f" <<PY
import io, sys
path = sys.argv[1]
with io.open(path, 'r', encoding='utf-8-sig') as src:
    data = src.read()
with io.open(path, 'w', encoding='utf-8') as dst:
    dst.write(data)
print('Normalized', path)
PY
  fi
done

if [ -f AT_Backend/fixtures.json ]; then
  echo "AT_Backend/fixtures.json found: loading data..."
  python manage.py loaddata AT_Backend/fixtures.json
elif [ -f fixtures.json ]; then
  echo "fixtures.json found at repo root: loading data..."
  python manage.py loaddata fixtures.json
else
  echo "no fixtures.json found"
fi

# Collect static files
python manage.py collectstatic --noinput

# Ensure admin user from env (idempotent)
if [ -n "$RENDER_ADMIN_USER" ] && [ -n "$RENDER_ADMIN_PASS" ]; then
  python - <<'PY'
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u = os.environ.get('RENDER_ADMIN_USER')
p = os.environ.get('RENDER_ADMIN_PASS')
e = os.environ.get('RENDER_ADMIN_EMAIL', 'admin@example.com')
if u and p:
    if not User.objects.filter(username=u).exists():
        User.objects.create_superuser(u, e, p)
        print('Created superuser', u)
    else:
        user = User.objects.filter(username=u).first()
        updated = False
        if not user.is_superuser:
            user.is_superuser = True
            updated = True
        if not user.is_staff:
            user.is_staff = True
            updated = True
        user.set_password(p)
        user.save()
        print('Superuser exists — password updated for', u)
        if updated:
            print('Also ensured staff/superuser flags for', u)
else:
    print('RENDER_ADMIN_USER or RENDER_ADMIN_PASS not set')
PY
fi

# Start gunicorn as the final step
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-file -
