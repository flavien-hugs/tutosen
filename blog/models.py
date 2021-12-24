# blog.models.py

import uuid
from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from utils import func_utils
from accounts.models import Teacher
from blog.managers import BlogPostManager

import readtime
from taggit.managers import TaggableManager


class Post(models.Model):
    uuid = models.UUIDField(
		db_index=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='post ID'
	)
    title = models.CharField(
    	verbose_name="title",
    	max_length=255,
    	help_text='add title for article'
    )
    subtitle = models.CharField(
    	verbose_name="subtitle",
    	max_length=255, blank=True,
    	help_text='add subtitle for article'
    )
    slug = models.SlugField(
    	verbose_name="post link",
    	max_length=255, unique=True
    )
    body = models.TextField(verbose_name="content")
    image = models.ImageField(
        verbose_name="post cover",
        blank=True, null=True,
        upload_to=func_utils.save_post_cover_file
    )
    created_at = models.DateTimeField(
    	verbose_name="date created",
    	auto_now_add=True
    )
    date_modified = models.DateTimeField(
    	verbose_name="date modified",
    	auto_now=True
    )
    published = models.BooleanField(
    	verbose_name="published",
    	default=False
    )
    author = models.ForeignKey(
    	verbose_name="author",
    	to=Teacher, on_delete=models.PROTECT
    )
    tags = TaggableManager(verbose_name="keywords")

    objects = BlogPostManager()

    class Meta:
        db_table = 'db_blog'
        ordering = ["-created_at"]
        get_latest_by = ['-created_at']
        verbose_name_plural = 'blog'
        indexes = [
            models.Index(fields=['id', 'uuid'], name='id_index_blog'),
        ]

    def __str__(self):
        return self.title

    def get_readtime(self):
        read_time_post = readtime.of_text(self.body)
        return read_time_post

    def get_absolute_url(self):
    	return reverse("blog:post_detail", kwargs={"slug": str(self.slug)})

    def get_post_list(self):
    	return reverse("blog:post_url", kwargs={"link": str(self.author.link)})

    def get_post_update(self):
    	return reverse(
    		"blogs:update_post_url",
    		kwargs={
    			"link": str(self.author.link),
    			"slug": str(self.slug)
    		}
    	)

    def get_post_delete(self):
    	return reverse(
    		"blogs:delete_post_url",
    		kwargs={
    			"link": str(self.author.link),
    			"slug": str(self.slug)
    		}
    	)


@receiver([models.signals.pre_save], sender=Post)
def subject_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = func_utils.unique_slug_generator(instance)

@receiver([models.signals.post_save], sender=Post)
def delete_old_image(sender, instance, *args, **kwargs):
    if hasattr(instance, '_current_image'):
        if instance._current_image != instance.image.path:
            instance._current_image.delete(save=False)
