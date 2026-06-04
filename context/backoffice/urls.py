from django.urls import path
from . import api_views

urlpatterns = [
    # Endpoints de administrador (solo admin)
    path('animes/', api_views.anime_list, name='anime_list'),
    path('animes/<int:pk>/', api_views.anime_detail, name='anime_detail'),
    path('mangas/', api_views.manga_list, name='manga_list'),
    path('mangas/<int:pk>/', api_views.manga_detail, name='manga_detail'),
    
    # Endpoints de episodios (autenticados)
    path('episodes/', api_views.episode_list, name='episode_list'),
    path('episodes/<int:pk>/', api_views.episode_detail, name='episode_detail'),
    
    # Endpoints públicos (todos los usuarios autenticados)
    path('public/animes/', api_views.public_anime_list, name='public_anime_list'),
    path('public/animes/<int:pk>/', api_views.public_anime_detail, name='public_anime_detail'),
    path('public/mangas/', api_views.public_manga_list, name='public_manga_list'),
    path('public/mangas/<int:pk>/', api_views.public_manga_detail, name='public_manga_detail'),
    path('public/mangas/<int:pk>/chapters/', api_views.public_manga_chapters, name='public_manga_chapters'),
    path('public/mangas/<int:pk>/chapters/<int:chapter_number>/', api_views.public_manga_chapter_pages, name='public_manga_chapter_pages'),
    path('public/animes/<int:pk>/likes/', api_views.update_anime_likes, name='update_anime_likes'),
    path('public/animes/<int:pk>/dislikes/', api_views.update_anime_dislikes, name='update_anime_dislikes'),
    
    # Jikan API Integration (solo admin)
    path('jikan/search/', api_views.jikan_search, name='jikan_search'),
    path('jikan/anime/<int:mal_id>/', api_views.jikan_anime_detail, name='jikan_anime_detail'),
    path('jikan/manga/search/', api_views.jikan_manga_search, name='jikan_manga_search'),
    path('jikan/manga/<int:mal_id>/', api_views.jikan_manga_detail, name='jikan_manga_detail'),
    
    # Consumet API Integration (usuarios autenticados)
    path('consumet/sources/<str:anime_slug>/<int:episode_number>/', api_views.get_consumet_sources, name='consumet_sources'),
    path('consumet/search/', api_views.search_consumet_anime, name='consumet_search'),
    path('consumet/episodes/<str:anime_id>/', api_views.get_consumet_episodes, name='consumet_episodes'),
    
    # Watch Progress (usuarios autenticados)
    path('progress/', api_views.user_progress_list, name='user_progress_list'),
    path('progress/<int:anime_id>/', api_views.anime_progress, name='anime_progress'),
    path('progress/<int:anime_id>/delete/', api_views.delete_progress, name='delete_progress'),
    
    # Analytics (usuarios autenticados)
    path('analytics/', api_views.analytics_metrics, name='analytics_metrics'),
]
