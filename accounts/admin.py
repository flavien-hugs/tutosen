# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import Teacher, TeacherMore, Student, StudentMore

User = get_user_model()


@admin.register(Teacher)
class UserAdmin(auth_admin.UserAdmin):
    date_hierarchy = 'date_joined'
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields':
            (   
                ("first_name", "last_name"),
                ("email", "type"),
                ("is_active", "is_staff"),
                ("date_joined", "last_login"),
            )}
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )

    list_display = [
        "get_fullname", "email",
        "type", "date_joined", "is_active"
    ]
    search_fields = ["get_fullname", 'email']
    list_display_links = [
        'email',
        'get_fullname',
    ]
    list_editable = (
        "is_active",
    )
    list_per_page = 5


@admin.register(Student)
class UserAdmin(auth_admin.UserAdmin):
    date_hierarchy = 'date_joined'
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields':
            (   
                ("first_name", "last_name"),
                ("email", "type"),
                ("is_active", "is_staff"),
                ("date_joined", "last_login"),
            )}
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'is_staff',
                    'is_active'
                )
            }
        ),
    )

    list_display = [
        "get_fullname", "email",
        "more",
        "type", "date_joined", "is_active"
    ]

    search_fields = ["get_fullname", 'email']
    list_display_links = [
        'email',
        'get_fullname',
    ]
    list_editable = (
        "is_active",
    )
    list_per_page = 5


admin.site.register(TeacherMore)
admin.site.register(StudentMore)
admin.site.unregister(Group)
