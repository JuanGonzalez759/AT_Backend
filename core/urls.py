
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import cors_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('context.accounts.api_urls')),
    path('api/manager/', include('context.manager.urls')),
    path('api/backoffice/', include('context.backoffice.urls')),
    path('', include('context.accounts.urls')),
    path('cors-test/', cors_test),
]

# Servir archivos media en desarrollo (videos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
