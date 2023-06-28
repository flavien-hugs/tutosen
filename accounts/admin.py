from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import Teacher, Student, ParentOrTutor


class CustomUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    date_hierarchy = "date_joined"

    fieldsets = (
        (
            "Information personnelle",
            {
                "fields": (
                    "type",
                    "email",
                    ("civility", "first_name", "last_name"),
                )
            },
        ),
        (
            "Adresse",
            {
                "classes": ("collapse",),
                "fields": (
                    "country",
                    "state",
                    "phone_number",
                ),
            },
        ),
        (
            "Descriprion",
            {
                "classes": ("collapse",),
                "fields": (
                    "statut",
                    "brief_desc",
                    "cover",
                ),
            },
        ),
        (
            "Compte réseaux sociaux",
            {
                "classes": ("collapse",),
                "fields": (
                    "facebook",
                    "twitter",
                    "linkedin",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                )
            },
        ),
        ("dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide", "extrapretty"),
                "fields": (
                    "email",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    list_display = [
        "colored_type",
        "email",
        "uppercase_name",
        "country",
        "get_teacher_courses_count",
        "account_verified",
        "show_user_url",
        "date_joined",
        "is_active",
    ]
    list_display_links = [
        "email",
        "uppercase_name",
    ]
    list_editable = ("is_active",)
    list_filter = (
        "date_joined",
        "is_active",
    )
    list_per_page = 10
    ordering = ["-date_joined"]
    actions = ["activate_account"]
    readonly_fields = ["show_user_url", "last_login", "date_joined"]
    search_fields = ["get_fullname", "email"]
    filter_horizontal = ["groups", "user_permissions"]

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                "is_superuser",
                "user_permissions",
            }

        if not is_superuser and obj is not None and obj == request.user:
            disabled_fields |= {
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    @admin.display(description="Nom & prénom")
    def uppercase_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".upper()

    @admin.display(description="activate account")
    def activate_account(self, request, queryset):
        queryset.update(is_active=True)

    @admin.display(description="teacher url", empty_value="???")
    def show_user_url(self, instance):
        if instance.type == "TEACHER":
            url = f"<a href='{instance.get_teacher_detail_url()}!r'>voir le profile</a>"
            return format_html(url)


@admin.register(Teacher)
class TeacherAdmin(CustomUserAdmin):
    model = Teacher

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        teachers = qs.filter(type="TEACHER")
        return teachers


@admin.register(Student)
class StudentAdmin(CustomUserAdmin):
    model = Student

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        teachers = qs.filter(type="STUDENT")
        return teachers


@admin.register(ParentOrTutor)
class ParentOrTutorAdmin(CustomUserAdmin):
    model = ParentOrTutor

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        teachers = qs.filter(type="PARENT_OR_TUTOR")
        return teachers
