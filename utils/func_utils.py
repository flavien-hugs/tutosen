# utils.func_utils.py

import os
import string
import random

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist


def random_string_generator(size=6, carac=string.digits):
    return ''.join(random.choice(carac) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        rand_key = random.randint(300_000, 500_000)
        new_slug = f"{slug}-{rand_key}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random_string_generator(8)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"image/course/{final_filename}"

def save_avatar_file(instance, filename):
    upload_to = 'image/users/'
    ext = filename.split('.')[-1]
    if instance.avatar:
        filename =  f"avatar_{instance.link}.{ext}"

    return os.path.join(upload_to, filename)

def save_cover_file(instance, filename):
    upload_to = 'image/users/'
    ext = filename.split('.')[-1]
    if instance.cover:
        filename =  f"cover_{instance.link}.{ext}"

    return os.path.join(upload_to, filename)

def save_chapiter_content_file(instance, filename):
    upload_to = 'image/'
    ext = filename.split('.')[-1]
    if instance.course.id:
        filename = f"chapiter_files/chapiter_{instance.course.slug}/{instance.course.slug}.{ext}"
        if os.path.exists(filename):
            new_name = str(instance.course.slug) + str('1')
            filename =  f"chapiter_files/chapiter_{instance.course.slug}/{new_name}.{ext}"
    return os.path.join(upload_to, filename)


def save_post_cover_file(instance, filename):
    upload_to = 'image/post/'
    ext = filename.split('.')[-1]
    if instance.image:
        filename =  f"article_{instance.slug}.{ext}"

    return os.path.join(upload_to, filename)


class CustomFields(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                queryset = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    queryset = queryset.filter(**query)
                last_item = queryset.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
