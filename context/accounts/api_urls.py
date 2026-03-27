from django.urls import path
from . import api_views

urlpatterns = [
    path('health/', api_views.health, name='api_health'),
    path('csrf/', api_views.csrf, name='api_csrf'),
    path('auth/register/', api_views.register_api, name='api_register'),
    path('auth/login/', api_views.login_api, name='api_login'),
    path('auth/logout/', api_views.logout_api, name='api_logout'),
    path('auth/user/', api_views.user_api, name='api_user'),
]
