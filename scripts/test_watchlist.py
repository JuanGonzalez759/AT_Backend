from context.manager.models import Profile, Watchlist
from context.backoffice.models import Manga

p = Profile.objects.first()
m = Manga.objects.first()
print('PROFILE:', getattr(p, 'id', None))
print('MANGA:', getattr(m, 'id', None))
if p is None or m is None:
    print('MISSING: no profile or no manga present')
else:
    w, created = Watchlist.objects.get_or_create(profile=p, manga=m)
    print('RESULT:', 'created' if created else 'exists', w.id)
