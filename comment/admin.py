# comment.admin.py

from django.contrib import admin

from comment import models


admin.site.register(models.Comment)
