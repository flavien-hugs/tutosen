# courses.models.py

import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import markdown as md
from utils import func_utils
from accounts import models as mdl


class Course(models.Model):
    LANGUAGE_CHOICES = (
        ('FR', 'Français'),
        ('ANG', 'Anglais')
    )
    COURSES_CATEGORY = (
        ('ANGL', 'Anglais'),
        ('FRAN', 'Français'),
        ('PHIL', 'Philosophie'),
        ('MATH', 'Mathématique'),
        ('PCHI', 'Physique/Chimie'),
        ('HIST', 'Histoire/Géographie'),
    )
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Cours ID'
    )
    instructor = models.ForeignKey(
        mdl.Teacher,
        models.SET_NULL,
        null=True,
        related_name='courses_created_by',
        verbose_name='instructeur'
    )
    student = models.ManyToManyField(
        mdl.Student,
        related_name='student_courses_enrolled',
        verbose_name='student joined course',
        blank=True
    )
    parent_or_tutor = models.ManyToManyField(
        mdl.ParentOrTutor,
        related_name='parent_or_tutor_courses_enrolled',
        verbose_name='parent or tutor joined course',
        blank=True
    )
    course_language = models.CharField(
        max_length=3,
        default="FR",
        choices=LANGUAGE_CHOICES,
        verbose_name='course language',
        help_text='language of course'
    )
    course_category = models.CharField(
        max_length=4,
        default="FRAN",
        choices=COURSES_CATEGORY,
        verbose_name='courses category',
        help_text='Aidez les gens à trouver\
        vos cours en choisissant des catégories\
        qui représentent votre cours.'
    )
    course_title = models.CharField(
        verbose_name='Course title',
        max_length=60,
        help_text='Rédigez un titre de cours de 60 caractères.'
    )
    course_brief = models.TextField(
        verbose_name='Brief course',
        help_text='Un bref résumé de votre cours.'
    )
    course_fee = models.PositiveIntegerField(
        verbose_name='course fee',
        help_text='add course fee'
    )
    slug = models.SlugField(
        verbose_name='link of course',
        help_text='link of course',
        blank=True, unique=True,
    )
    published = models.BooleanField(
        verbose_name='course published',
        default=False,
    )
    published_date = models.DateField(
        verbose_name='published date',
        auto_now_add=False,
        blank=True, null=True
    )
    date_created = models.DateField(
        verbose_name='date add of courses',
        auto_now_add=True
    )

    class Meta:
        db_table = 'course_db'
        ordering = ['-date_created']
        get_latest_by = ['-date_created']
        verbose_name_plural = 'courses'

    def __str__(self):
        return '{}'.format(self.course_brief)

    def get_absolute_url(self):
        return reverse(
            'course:cours_detail',
            kwargs={
                'slug': str(self.slug),
                'pk': str(self.uuid)
            }
        )

    def get_course_delete_url(self):
        return reverse(
            'boards:course_delete',
            kwargs={
                'slug': str(self.slug),
                'pk': str(self.uuid)
            }
        )

    def get_course_update_url(self):
        return reverse(
            'boards:course_update',
            kwargs={
                'slug': str(self.slug),
                'pk': str(self.uuid)
            }
        )


class CourseChapter(models.Model):
    course = models.ForeignKey(
        Course, models.SET_NULL, null=True,
        verbose_name='course'
    )
    chapter_title = models.CharField(
        verbose_name='chapter title',
        max_length=200,
        help_text='add chapter title'
    )
    chapter_desc = models.TextField(
        blank=True,
        verbose_name='chapter description',
        help_text='add chapter description'
    )
    chapter_order = func_utils.CustomFields(
        blank=True,
        verbose_name='chapter number',
        for_fields=['chapter_title']
    )

    class Meta:
        ordering = ['chapter_order']
        db_table = 'course_chapter_db'
        verbose_name_plural = 'course chapiter'

    def __str__(self):
        return "{0}-{1}".format(self.chapter_order, self.chapter_title)


class CourseChapterContent(models.Model):
    chapter_content = models.ForeignKey(
        CourseChapter,
        models.CASCADE,
        verbose_name='course chapter',
        related_name='course_chapter_content',
    )
    chapter_type_content = models.ForeignKey(
        ContentType, 
        models.CASCADE,
        limit_choices_to={
            'model__in':(
                'text', 'video',
                'image', 'file'
            )
        }
    )
    chapter_id = models.PositiveIntegerField()
    chapter_item = GenericForeignKey('chapter_type_content', 'chapter_id')
    chapter_content_order = func_utils.CustomFields(
        blank=True,
        verbose_name='chapter number',
        for_fields=['course_chapter']
    )

    class Meta:
        db_table = 'course_chapter_content_db'
        ordering = ['chapter_content_order']
        verbose_name_plural = 'course chapter content'


class ChapterTypeContent(models.Model):
    instructeur = models.ForeignKey(
        mdl.Teacher, models.CASCADE,
        related_name='%(class)s_related'
    )
    content_type_title = models.CharField(
        verbose_name='content title', max_length=250,
        help_text='define content type title'
    )
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='date updated', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{0}".format(self.content_type_title)

    def render_content(self):
        content = 'course/content/{0}.html'.format(self._meta.model_name)
        ctx = {'item': self}
        return render_to_string(content, ctx)


class TextContent(ChapterTypeContent):
    content = models.TextField(verbose_name='content description')

    def __str__(self):
        truncated_ctn = Truncator(self.content)
        truncated_ctn_chars = truncated_ctn.chars(30)
        return "{0} {1}".format(self.get_fullname(), truncated_ctn_chars)

    def get_description_as_markdown(self):
        markdown_render = md.markdown(
            self.content or u'',
            extensions=['markdown.extensions.fenced_code']
        )
        return markdown_render


class File(ContentType):
    doc = models.FileField(
        verbose_name='upload file', upload_to='file/', help_text='upload file'
    )


class Image(ContentType):
    img = models.ImageField(
        verbose_name='upload image', upload_to='img/', help_text='upload image'
    )


class Movie(ContentType):
    movie_url = models.URLField(verbose_name='add movies url')
