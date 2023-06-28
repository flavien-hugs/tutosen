from django.contrib import admin

from product.models import Product

from django_summernote.admin import SummernoteModelAdmin


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    model = Product
    list_per_page = 10
    date_hierarchy = "created_at"

    list_display = (
        "id",
        "title",
        "price",
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
