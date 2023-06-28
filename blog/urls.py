# blog.urls.py

from django.urls import path

from blog import views as blog_views

app_name = "blog"
urlpatterns = [
    path(route="", view=blog_views.blog_post_list_view, name="post_list"),
    path(route="post/json/", view=blog_views.ajax_post_view, name="ajax_post_view"),
    path(route="<slug>/", view=blog_views.blog_post_detail_view, name="post_detail"),
]
