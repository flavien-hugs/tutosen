# core.urls.py

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from django.views import generic

admin.site.site_header = "TUTOSEN"
admin.site.site_title = "TUTOSEN"
admin.site.index_title = "WELCOME TO TUTOSEN"


def handler404(request, exception, template_name='404.html'):
    return render(request, template_name=template_name, status=404,
        context={'page_title': 'Page non trouvée'})

def handler403(request, exception, template_name='403.html'):
    return render(request, template_name=template_name, status=403,
        context={'page_title': 'Page non trouvée'})

def handler500(request, template_name='500.html'):
    return render(request, template_name=template_name,
        status=500, context={'page_title': 'Erreur interne'})


urlpatterns = [
	path('', generic.TemplateView.as_view(template_name='index.html'), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('boards.urls', namespace='boards')),
    path('cours/', include('courses.urls', namespace='courses')),
    path('sp-', include('pages.urls', namespace='pages')),

	path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('tinymce/', include('tinymce.urls')),
    path('x-tutosen/', admin.site.urls),
]

handler404 = handler404
handler403 = handler403
handler201600 = handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('404', handler404, {'exception': Exception()}),
        path('403', handler403, {'exception': Exception()}),
        path('500', handler500),
    ]
