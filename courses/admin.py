# courses.admin.py

from django.contrib import admin

from courses.models import Course


admin.site.register(Course)
