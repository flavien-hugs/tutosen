# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Teacher, TeacherMore, StudentMore
from accounts.forms import UserChangeForm, UserCreationForm

CustomUser = get_user_model()


# class TeacherMoreInline(admin.StackedInline):
#     model = TeacherMore
#     can_delete = False
#     verbose_name_plural = 'Instructeur détail'


# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     inlines = [TeacherMoreInline]


@admin.register(CustomUser)
class TeacherAdmin(BaseUserAdmin):
    date_hierarchy = 'date_joined'
    model = CustomUser
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': (("type", "email"),)}),
        ('Information personnelle', {'fields': ('username', ('first_name', 'last_name'),)}),
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
        "type", "date_joined", "is_active"
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
    ordering = ('date_joined',)
    search_fields = ["get_fullname", 'email']
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(TeacherMore)
admin.site.register(StudentMore)
admin.site.unregister(Group)
