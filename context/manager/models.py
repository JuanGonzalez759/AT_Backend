from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1, message="El nombre no puede estar vacío")]
    )
    avatar = models.CharField(max_length=255, default='/profiles/Profile1.png')
    background = models.CharField(max_length=500, default='')
    color = models.CharField(max_length=7, default='#000000')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.name}'


class Watchlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='watchlist')
    anime = models.ForeignKey('backoffice.Anime', on_delete=models.CASCADE, related_name='in_watchlists', null=True, blank=True)
    manga = models.ForeignKey('backoffice.Manga', on_delete=models.CASCADE, related_name='in_watchlists_manga', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
        # uniqueness enforced at API level for (profile, anime) or (profile, manga)
        verbose_name = 'Watchlist Item'
        verbose_name_plural = 'Watchlist Items'

    def __str__(self):
        title = None
        if self.anime_id and getattr(self.anime, 'title', None):
            title = self.anime.title
        elif self.manga_id and getattr(self.manga, 'title', None):
            title = self.manga.title
        return f'{self.profile.name} - {title or "item"}'
