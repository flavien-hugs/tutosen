# core.urls.py

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

admin.site.site_header = "TUTOSEN"
admin.site.site_title = "TUTOSEN"
admin.site.index_title = "WELCOME TO TUTOSEN"


urlpatterns = [
	path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('tinymce/', include('tinymce.urls')),
    path('x-tutosen/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
