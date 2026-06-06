import os
import sys
from pathlib import Path
import shutil

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.conf import settings
from context.backoffice.models import Page
from django.core.management import call_command

uploads_root = repo_root.parent / 'uploads'

def find_in_uploads(basename):
    for root, dirs, files in os.walk(uploads_root):
        if basename in files:
            return Path(root) / basename
    return None

def restore_files():
    restored = 0
    for p in Page.objects.all():
        if not p.image:
            continue
        rel = p.image.name
        local_path = Path(settings.MEDIA_ROOT) / rel
        if local_path.exists():
            continue
        basename = os.path.basename(rel)
        found = find_in_uploads(basename)
        if not found:
            print(f'Not found in uploads: {basename}')
            continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(found, local_path)
        print(f'Restored {basename} -> {local_path}')
        restored += 1
    print(f'Restored total: {restored}')
    return restored


if __name__ == '__main__':
    if not uploads_root.exists():
        print('uploads directory not found:', uploads_root)
        sys.exit(1)
    print('Scanning pages and restoring missing files from uploads...')
    restore_files()
    print('Running migration to upload to Cloudinary and delete local copies...')
    call_command('migrate_pages_to_cloudinary', '--delete-local')
