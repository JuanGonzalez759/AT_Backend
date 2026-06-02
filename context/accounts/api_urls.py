from django.urls import path
from . import api_views

urlpatterns = [
    path('health/', api_views.health, name='api_health'),
    path('auth/register/', api_views.register_api, name='api_register'),
    path('auth/login/', api_views.login_api, name='api_login'),
    path('auth/logout/', api_views.logout_api, name='api_logout'),
    path('auth/user/', api_views.user_api, name='api_user'),
    path('auth/password-reset/request/', api_views.request_password_reset, name='api_password_reset_request'),
    path('auth/password-reset/verify/', api_views.verify_reset_token, name='api_password_reset_verify'),
    path('auth/password-reset/confirm/', api_views.reset_password, name='api_password_reset_confirm'),
    path('users/', api_views.list_users, name='api_users_list'),
    path('chat/<int:user_id>/messages/', api_views.messages_between, name='api_chat_messages'),
]
