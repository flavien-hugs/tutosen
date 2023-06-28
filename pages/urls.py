# pages.urls.py

from django.urls import path

from pages import views as pages_views


app_name = "pages"
urlpatterns = [
    path(route="contact/", view=pages_views.contact_view, name="contact"),
    path(route="qui-sommes-nous/", view=pages_views.page_aboutus_view, name="about_us"),
    path(
        route="conditition-generale-utilisation/",
        view=pages_views.page_cgu_detail,
        name="page_cgu",
    ),
    path(route="support/", view=pages_views.page_support_detail, name="page_support"),
]
