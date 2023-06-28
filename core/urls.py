# core.urls.py

from django.contrib import admin
from django.conf import settings
from django.views import generic
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from courses.models import Subject
from courses.mixins import CourseSearchMixin
from accounts.mixins import TeacherSearchMixin
from django_summernote.models import Attachment

admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(Attachment)


admin.site.site_header = "Unsta Inc School"
admin.site.site_title = admin.site.site_header
admin.site.index_title = f"WELCOME TO {admin.site.site_header} Dashboard"


def handler404(request, exception, template_name="404.html"):
    context = {"page_title": "Page non trouvée"}
    return render(request, template_name, context, status=404)


def handler403(request, exception, template_name="403.html"):
    context = {"page_title": "Permission non accordée"}
    return render(request, template_name, context, status=403)


def handler500(request, template_name="500.html"):
    context = {"page_title": "Erreur interne"}
    return render(request, template_name, context, status=500)


class HomeView(generic.TemplateView):
    template_name = "index.html"


home_view = HomeView.as_view()


urlpatterns = [
    path(route="", view=home_view, name="home"),
    path("me/", include("boards.urls")),
    path("courses/", include("courses.urls")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("pages/", include("pages.urls", namespace="pages")),
    path("summernote/", include("django_summernote.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/v1/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "robots.txt",
        generic.TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
]

handler404 = handler404
handler403 = handler403
handler500 = handler500

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path("404/", handler404, {"exception": Exception("Page non trouvée !")}),
        path("403/", handler403, {"exception": Exception("Permission non accordée !")}),
        path("500/", handler500),
    ]
