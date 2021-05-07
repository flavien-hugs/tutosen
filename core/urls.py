# core.urls.py

from django.contrib import admin
from django.conf import settings
from django.views import generic
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static

admin.site.site_header = "TUTOSEN"
admin.site.site_title = "TUTOSEN"
admin.site.index_title = "WELCOME TO TUTOSEN"


def handler404(request, exception, template_name='404.html'):
    context = {'page_title': 'Page non trouvée'}
    return render(request, template_name, context, status=404)


def handler403(request, exception, template_name='403.html'):
    context = {'page_title': 'Permission non accordée'}
    return render(request, template_name, context, status=403)


def handler500(request, template_name='500.html'):
    context = {'page_title': 'Erreur interne'}
    return render(request, template_name, context, status=500)


urlpatterns = [
    path('', generic.TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/v1/', include('api.urls')),
    path('dashboard/', include('boards.urls', namespace='boards')),
    path('cours/', include('courses.urls', namespace='courses')),
    path('sp-', include('pages.urls', namespace='pages')),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

handler404 = handler404
handler403 = handler403
handler201600 = handler500

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('404/', handler404, {'exception': Exception("Page non trouvée !")}),
        path('403/', handler403, {'exception': Exception("Permission non accordée !")}),
        path('500/', handler500, {'exception': Exception("Erreur interne !")}),
    ]

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
