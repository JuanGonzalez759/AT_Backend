import os
import sys
from pathlib import Path
import django

# Ensure AT_Backend is on sys.path so `core` settings module can be imported
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from context.backoffice.models import Page

import os
from decouple import config

print('CLOUDINARY_URL in os.environ:', bool(os.environ.get('CLOUDINARY_URL')))
try:
	v = config('CLOUDINARY_URL', default='')
	print('decouple.config CLOUDINARY_URL non-empty:', bool(v))
except Exception as e:
	print('decouple.config check error:', e)

urls = [p.image.url for p in Page.objects.all()[:10]]
print(urls)
if Page.objects.exists():
	p = Page.objects.first()
	storage = p.image.storage
	print('Storage class:', storage.__class__)
	try:
		print('Storage module:', storage.__class__.__module__)
	except Exception:
		pass
	try:
		print('Sample URL:', p.image.url)
	except Exception as e:
		print('Error getting URL:', e)
