import os
import django
from pathlib import Path
import sys

env_path = Path(__file__).resolve().parent.parent
sys.path.append(str(env_path))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from context.backoffice.models import Manga, Chapter, Page
from django.core.files import File
from django.conf import settings

UPLOAD_DIR = Path(r'C:/AniTokiii/uploads/onepiece_ch1050')
MANGA_ID = 1
CHAPTER_NUMBER = 1
CHAPTER_TITLE = 'Capítulo 1'
LANGUAGE = 'es'

print('Starting import from', UPLOAD_DIR)
if not UPLOAD_DIR.exists():
    print('Upload dir not found:', UPLOAD_DIR)
    sys.exit(1)

manga = Manga.objects.filter(pk=MANGA_ID).first()
if not manga:
    print('Manga id', MANGA_ID, 'not found')
    sys.exit(1)

# create or get chapter
chapter, created = Chapter.objects.get_or_create(manga=manga, number=CHAPTER_NUMBER, defaults={'title': CHAPTER_TITLE, 'language': LANGUAGE})
print('Chapter', chapter, 'created' if created else 'exists')

# list files ordered
files = sorted([p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in ['.jpg','.jpeg','.png','.webp']])
if not files:
    print('No image files found in upload dir')
    sys.exit(1)

for idx, fpath in enumerate(files, start=1):
    # destination path inside MEDIA
    subdir = Path('mangas')/str(manga.id)/'chapters'/str(chapter.number)
    dest_dir = Path(settings.MEDIA_ROOT)/subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / fpath.name
    # copy file
    with open(fpath, 'rb') as srcf:
        with open(dest_path, 'wb') as dstf:
            dstf.write(srcf.read())
    # save Page
    relative_path = subdir/ fpath.name
    # check if page exists
    if not chapter.pages.filter(page_number=idx).exists():
        page = Page(chapter=chapter, page_number=idx)
        with open(dest_path, 'rb') as imgf:
            django_file = File(imgf)
            page.image.save(str(relative_path), django_file, save=True)
        print('Saved page', idx)
    else:
        print('Page', idx, 'already exists')

print('Import completed')
