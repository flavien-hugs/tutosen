# blog.admin.py

from django.contrib import admin

from blog.models import Post
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    model = Post
    list_per_page = 10
    date_hierarchy = "created_at"

    list_display = (
        "id",
        "title",
        "tag_list",
        "created_at",
        "published",
    )
    list_display_links = [
        "id",
        "title",
    ]
    list_filter = (
        "published",
        "created_at",
    )
    list_editable = ("published",)
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
