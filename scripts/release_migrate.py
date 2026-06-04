import os
import time
import sys
import subprocess

import psycopg2

DB_URL = os.environ.get('DATABASE_URL')
if not DB_URL:
    print('DATABASE_URL not set; exiting')
    sys.exit(1)

max_attempts = int(os.environ.get('DB_WAIT_ATTEMPTS', '60'))
wait_seconds = int(os.environ.get('DB_WAIT_SECONDS', '2'))

print(f"Waiting for database to be available (attempts={max_attempts}, wait={wait_seconds}s)...")
for attempt in range(1, max_attempts + 1):
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=5)
        conn.close()
        print('Database is available')
        break
    except Exception as e:
        print(f'Attempt {attempt}/{max_attempts} failed: {e}')
        if attempt == max_attempts:
            print('Max attempts reached, exiting with error')
            sys.exit(1)
        time.sleep(wait_seconds)

# Run migrations
print('Running migrations...')
ret = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'])
if ret.returncode != 0:
    print('migrate command failed')
    sys.exit(ret.returncode)

# Collect static files
print('Collecting static files...')
ret = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
if ret.returncode != 0:
    print('collectstatic failed')
    sys.exit(ret.returncode)

print('Release tasks completed successfully')
