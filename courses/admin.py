# courses.admin.py

from django.contrib import admin

from courses.models import Subject, Course, CourseChapter
from django_summernote.admin import SummernoteModelAdmin


class CourseChapterAdmin(admin.StackedInline):
    model = CourseChapter
    extra = 1
    readonly_fields = ["order"]
    fieldsets = (
        (
            "Course information",
            {
                "classes": ("collapse",),
                "fields": (("order", "title"), ("movie", "document"), "chapter_desc"),
            },
        ),
    )
    verbose_name_plural = "Lessons"


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    model = Course
    date_hierarchy = "created_at"
    extra = 1
    readonly_fields = ["order"]
    inlines = [CourseChapterAdmin]
    verbose_name_plural = "Courses"


@admin.register(Subject)
class SubjectAdmin(SummernoteModelAdmin):
    model = Subject
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Subject information",
            {
                "classes": ("collapse",),
                "fields": (
                    "level",
                    ("language", "category"),
                    ("title", "slug"),
                    "published",
                ),
            },
        ),
        (
            "Course description",
            {"classes": ("collapse",), "fields": ("description", "image")},
        ),
    )
    list_per_page = 10
    list_editable = ["published"]
    list_display_links = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = [
        "title",
        "level",
        "language",
        "category",
    ]
    list_filter = ["level", "language", "category", "created_at"]
    list_display = [
        "title",
        "category",
        "count_subjects_course",
        "created_at",
        "published",
    ]
