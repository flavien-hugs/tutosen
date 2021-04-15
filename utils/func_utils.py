# utils.func_utils.py

import os
import string
import random
from django.utils.text import slugify


def random_string_generator(size=8, carac=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(carac) for _ in range(size))


def unique_key_generator(instance):
    size = random.randint(20, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qsx = Klass.objects.filter(key=key).exists()
    if qsx:
        return unique_slug_generator(instance)
    return key


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.cours_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=8)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random_string_generator(8)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(
        new_filename=new_filename,
        ext=ext
    )
    return "image/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )
