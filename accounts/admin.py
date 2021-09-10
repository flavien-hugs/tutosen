# accounts.admin.py

from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import UserChangeForm, UserCreationForm


@admin.register(get_user_model())
class TeacherAdmin(BaseUserAdmin):
    form = UserChangeForm
    model = get_user_model()
    add_form = UserCreationForm
    date_hierarchy = 'date_joined'

    fieldsets = (
        (
            'Information personnelle',
            {'fields': ("type", 'username', ('first_name', 'last_name'),)}
        ),
        (
            'Adresse', {
                'classes': ('collapse',),
                'fields': ("country", "state", "phone_number", "email",)
            }
        ),
        (
            'Descriprion', {
                'classes': ('collapse',),
                'fields': ("brief_desc", 'cover',)
            }
        ),
        (
            'Compte réseaux sociaux', {
                'classes': ('collapse',),
                'fields': ("facebook", "twitter", "linkedin",)
            }
        ),
        (
            'Permissions',
            {'fields': ("is_active", "is_staff", "is_superuser", "user_permissions",)}
        ),
        ('dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('email', 'is_staff', 'is_active',)
        }),
    )

    list_display = [
        "colored_type", "get_fullname", "email",
        "country", "account_verified", "show_user_url",
        "date_joined", "is_active",
    ]
    list_display_links = [
        'email',
        'get_fullname',
    ]
    list_editable = (
        "is_active",
    )
    list_filter = (
        "type",
        "date_joined",
        "is_active",
    )
    list_per_page = 10
    ordering = ['-date_joined']
    readonly_fields = ['show_user_url', 'last_login', 'date_joined']
    search_fields = ["get_fullname", 'email']
    filter_horizontal = ['groups', 'user_permissions']

    def show_user_url(self, instance):
        if instance.type == 'TEACHER':
            url = reverse('accounts:teacher_detail_view', kwargs={'uuid': str(instance.uuid)})
            response = format_html("""<a href="{0}">{0}</a>""", url)
        else:
            response = 'Not URL'
        return response
    show_user_url.short_description = "User URL"


admin.site.unregister(Group)
