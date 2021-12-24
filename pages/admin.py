# pages.admin.py

from django.contrib import admin

from pages import models


admin.site.register(models.AboutUs)
admin.site.register(models.PageCGU)
admin.site.register(models.PageSupport)
admin.site.register(models.Newsletters)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    model = models.Contact
    date_hierarchy = 'date_added'
    fieldsets = (
        (
            'adresse', {
                'classes': ('collapse',),
                'fields': (
                    ('first_name', 'last_name'),
                    ("email", "phone"),
                )
            }
        ),
        (
            'message',
            {'fields': ('reason', 'message',)}
        ),
    )
    list_per_page = 10
    list_filter = ["reason"]
    list_display_links = ["first_name", "email"]
    list_display = ["first_name", "email", "reason", "date_added"]
    readonly_fields = ['first_name', 'last_name', 'phone', 'email', 'reason', 'message']
