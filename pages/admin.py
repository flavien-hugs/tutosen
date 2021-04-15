# pages.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group

from pages.models import AboutUs, PageCGU, PageSupport


admin.site.register(AboutUs)
admin.site.register(PageCGU)
admin.site.register(PageSupport)


admin.site.unregister(Group)
