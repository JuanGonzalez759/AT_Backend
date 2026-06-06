from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from django.conf import settings
from context.backoffice.models import Page
import os


class Command(BaseCommand):
    help = 'Upload Page.image files from local MEDIA_ROOT to configured default storage (Cloudinary) and update DB.'

    def add_arguments(self, parser):
        parser.add_argument('--delete-local', action='store_true', help='Delete local file after successful upload')

    def handle(self, *args, **options):
        delete_local = options.get('delete_local', False)

        pages = Page.objects.all()
        total = pages.count()
        uploaded = 0
        skipped = 0
        errors = 0

        self.stdout.write(self.style.NOTICE(f'Starting migration of {total} Page objects...'))

        for p in pages:
            if not p.image:
                skipped += 1
                continue

            try:
                url = ''
                try:
                    url = p.image.url
                except Exception:
                    url = ''

                # If already on Cloudinary (common domain), skip
                if url and 'res.cloudinary.com' in url:
                    self.stdout.write(self.style.SUCCESS(f'Skipping (already cloud): {p} -> {url}'))
                    skipped += 1
                    continue

                # Determine local file path
                name = p.image.name
                local_path = os.path.join(settings.MEDIA_ROOT, name)
                if not os.path.exists(local_path):
                    # Try repository-level uploads/ (in case MEDIA_ROOT wasn't used)
                    repo_root = settings.BASE_DIR.parent if hasattr(settings, 'BASE_DIR') else None
                    if repo_root:
                        alt = os.path.join(repo_root, 'uploads', name)
                        if os.path.exists(alt):
                            local_path = alt

                if not os.path.exists(local_path):
                    self.stdout.write(self.style.WARNING(f'Local file not found for {p}: {local_path}'))
                    errors += 1
                    continue

                # Open and save via storage (this will upload to Cloudinary when DEFAULT_FILE_STORAGE is set)
                with open(local_path, 'rb') as f:
                    django_file = DjangoFile(f)
                    # Use same filename
                    filename = os.path.basename(local_path)
                    p.image.save(filename, django_file, save=True)

                uploaded += 1
                self.stdout.write(self.style.SUCCESS(f'Uploaded {p} -> {p.image.url}'))

                if delete_local:
                    try:
                        os.remove(local_path)
                        self.stdout.write(self.style.NOTICE(f'Deleted local file {local_path}'))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Could not delete local file {local_path}: {e}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error migrating {p}: {e}'))
                errors += 1

        self.stdout.write('---')
        self.stdout.write(f'Total: {total}, Uploaded: {uploaded}, Skipped: {skipped}, Errors: {errors}')
