# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Teacher, Student
from accounts.forms import UserChangeForm, UserCreationForm

CustomUser = get_user_model()


@admin.register(Teacher)
class TeacherAdmin(BaseUserAdmin):
    date_hierarchy = 'date_joined'
    model = Teacher
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (

        ('Information personnelle',
            {'fields': 
                ("type", 'username', ('first_name', 'last_name'),)
            }
        ),
        ('Adresse', {'fields': 
            ("country", "state", "phone_number", "email",)
        }),
        ('Descriprion', {'fields': ("brief_desc",)}),
        ('Compte réseaux sociaux', {'fields': 
            ("facebook", "twitter", "linkedin",)
        }),
        ('Permissions', {'fields': 
            ( "is_active", "is_staff", "is_superuser", "user_permissions",)
        }),
        ('dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('email', 'is_staff', 'is_active',)
        }),
    )

    list_display = [
        "get_fullname", "email",
        "country", "date_joined",
        "is_active",
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
    list_per_page = 5
    ordering = ['-date_joined',]
    search_fields = ["get_fullname", 'email']
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Student)
admin.site.unregister(Group)
