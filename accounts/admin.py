# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from accounts.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    date_hierarchy = 'date_joined'
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "first_name", "last_name", "email",
        "type", "date_joined"
    ]
    search_fields = ["first_name", 'email']
    list_display_links = [
        'email',
        'last_name', 'first_name',
    ]
    list_per_page = 5

admin.site.unregister(Group)
