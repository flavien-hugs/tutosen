# courses.models.py

import uuid
import datetime

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import Truncator
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import markdown as md
from utils import func_utils
from accounts import models as mdl

# from comment.models import Comment

from courses.managers import SubjectManager


class Subject(models.Model):
    LANGUAGE_CHOICES = (("FR", "Français"), ("ANG", "Anglais"))
    SUBJECT_CATEGORY = (
        ("ANGL", "Anglais"),
        ("FRAN", "Français"),
        ("PHIL", "Philosophie"),
        ("MATH", "Mathématique"),
        ("CHIM", "Chimie"),
        ("PHYS", "Physique"),
        ("HIST", "Histoire"),
        ("GEOG", "Géographie"),
    )
    SUBJECT_LEVEL = (
        ("6ième", "6ième"),
        ("5ième", "5ième"),
        ("4ième", "4ième"),
        ("3ième", "3ième"),
        ("2nde C", "2nde C"),
        ("2nde A", "2nde A"),
        ("1ère A", "1ère A"),
        ("1ère D", "1ère D"),
        ("1ère C", "1ère C"),
        ("Tle A", "Tle A"),
        ("Tle D", "Tle D"),
        ("Tle C", "Tle C"),
    )
    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, verbose_name="Subject ID"
    )
    title = models.CharField(
        verbose_name="Subject title",
        max_length=60,
        help_text="ajouter un titre de 60 caractères.",
    )
    subtitle = models.CharField(
        verbose_name="Subject sub-title",
        max_length=200,
        blank=True,
        null=True,
        help_text="ajouter un sous-titre de 200 caractères.",
    )
    price = models.PositiveIntegerField(
        default=1500, verbose_name="course price", help_text="add course price"
    )
    sale_price = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="course sale price",
        help_text="add course sale price",
    )
    language = models.CharField(
        max_length=3,
        default="FR",
        choices=LANGUAGE_CHOICES,
        verbose_name="course language",
        help_text="language of course",
    )
    category = models.CharField(
        max_length=4,
        default="FRAN",
        choices=SUBJECT_CATEGORY,
        verbose_name="course category",
        help_text="définir la catégorie qui représentent votre cours.",
    )
    level = models.CharField(
        max_length=6,
        default="6ième",
        choices=SUBJECT_LEVEL,
        verbose_name="course level",
        help_text="le niveau qui représentent votre cours.",
    )
    description = models.TextField(
        verbose_name="subject description",
        blank=True,
        null=True,
        help_text="subject description. Who user learn ?",
    )
    resume = models.TextField(
        verbose_name="subject resume",
        blank=True,
        null=True,
        help_text="subject resume.",
    )
    image = models.ImageField(
        verbose_name="subject cover",
        upload_to=func_utils.upload_image_path,
        blank=True,
        null=True,
        help_text="upload subject cover",
    )
    slug = models.SlugField(
        verbose_name="link of subject",
        help_text="link of subject",
        blank=True,
        unique=True,
    )
    free = models.BooleanField(
        verbose_name="subject is free ?",
        default=False,
        help_text="this subject is free ?",
    )
    published = models.BooleanField(
        verbose_name="subject published ?",
        default=False,
        help_text="this course is published ?",
    )
    created_at = models.DateField(
        verbose_name="created at", auto_now_add=True, auto_now=False
    )
    update_at = models.DateTimeField(
        verbose_name="updated at", auto_now=True, auto_now_add=False
    )

    objects = SubjectManager()

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = ["-created_at"]
        verbose_name_plural = "sujets"
        indexes = [
            models.Index(fields=["id", "uuid"]),
        ]

    def __str__(self):
        return f"{self.title}"

    @mark_safe
    @admin.display(description="course description")
    def course_description(self):
        return self.description

    @admin.display(
        boolean=True, ordering="created_at", description="published recently ?"
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    @admin.display(description="course publish")
    def publish_now(self):
        return not datetime.date.today() > self.created_at

    # chapters in course
    @admin.display(description="chapters in course", empty_value="???")
    def subject_courses(self):
        chapters = Course.objects.filter(subject=self).order_by("order")
        return chapters

    @admin.display(description="courses number", empty_value="???")
    def count_subjects_course(self):
        count_courses = self.subject_courses().count()
        return count_courses

    # lessons in chapter
    @admin.display(description="lessons in chapiter", empty_value="???")
    def get_lessons(self):
        lessons = CourseChapter.objects.filter(course__in=self.subject_courses())
        return lessons

    @admin.display(description="total lessons", empty_value="???")
    def get_lessons_count(self):
        count_lessons = self.get_lessons().count()
        return count_lessons

    @admin.display(description="comment for course", empty_value="???")
    def get_comments(self):
        from comment.models import Comment

        comments = Comment.objects.filter(course=self)
        return comments

    @admin.display(description="number for course", empty_value="???")
    def get_comments_count(self):
        comments_count = self.get_comments().aggregate(count=models.Count("id"))
        counter = 0
        if comments_count["count"] is not None:
            counter = int(comments_count["count"])
        return counter

    # calcul de la moyenne des note de commentaire
    @admin.display(description="comment rating")
    def feedback_avarege(self):
        feedback = self.get_comments().aggregate(rating=models.Avg("rate"))
        average = 0
        if feedback["rating"] is not None:
            average = "%.1f" % float(feedback["rating"])
        return average

    def feeback_average_percent(self):
        percent = "%.0f" % (float(self.feedback_avarege()) * 10)
        return percent

    def get_absolute_url(self):
        return reverse(
            "feedback:detail_feedback_url",
            kwargs={
                "link": str(self.course.instructor.link),
                "course_slug": self.course.slug,
            },
        )

    def get_absolute_url(self):
        kwargs = {"slug": str(self.slug)}
        return reverse("courses:course_detail", kwargs=kwargs)

    def get_subject_list_url(self):
        return reverse(
            "subject:list_subject_url", kwargs={"link": str(self.instructor.link)}
        )

    def get_subject_update_url(self):
        return reverse(
            "subject:update_subject_url",
            kwargs={"link": str(self.instructor.link), "slug": str(self.slug)},
        )

    def get_subject_delete_url(self):
        return reverse(
            "subject:delete_subject_url",
            kwargs={"link": str(self.instructor.link), "slug": str(self.slug)},
        )

    def get_subject_course_list_url(self):
        return reverse(
            "course:list_course_url",
            kwargs={"link": str(self.instructor.link), "slug": str(self.slug)},
        )

    def get_subject_chapiter_create_url(self):
        return reverse(
            "course:create_course_url",
            kwargs={"link": str(self.instructor.link), "slug": str(self.slug)},
        )

    def get_comment_detail_url(self):
        return reverse(
            "feedback:detail_feedback_url",
            kwargs={"link": self.instructor.link, "slug": self.slug},
        )


class Course(models.Model):
    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, verbose_name="Cours ID"
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        related_name="subjects",
        verbose_name="subject",
    )
    order = func_utils.CustomFields(
        blank=True, verbose_name="chapiter number", for_fields=["subject"]
    )
    title = models.CharField(
        verbose_name="chapter title",
        max_length=60,
        help_text="Rédigez un titre de cours de 60 caractères.",
    )
    description = models.TextField(
        verbose_name="chapiter description",
        blank=True,
        null=True,
        help_text="chapiter description",
    )
    slug = models.SlugField(
        verbose_name="link this chapiter",
        help_text="link this chapiter",
        blank=True,
        unique=True,
    )
    created_at = models.DateField(
        verbose_name="date created of courses", auto_now_add=True, auto_now=False
    )
    update_at = models.DateTimeField(
        verbose_name="date updated of courses", auto_now=True, auto_now_add=False
    )

    class Meta:
        ordering = ["order"]
        get_latest_by = ["created_at", "update_at"]
        verbose_name_plural = "cours"
        indexes = [
            models.Index(fields=["id", "uuid"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "lessons:chapiter_detail",
            kwargs={
                "slug": str(self.subject.slug),
                "chapiter_slug": str(self.slug),
                "pk": str(self.pk),
            },
        )

    def get_course_list_url(self):
        return reverse(
            "course:list_course_url",
            kwargs={
                "link": str(self.subject.instructor.link),
                "slug": str(self.subject.slug),
            },
        )

    def get_chapiter_update_url(self):
        return reverse(
            "course:update_course_url",
            kwargs={
                "link": str(self.subject.instructor.link),
                "slug": str(self.subject.slug),
                "pk": str(self.pk),
            },
        )

    def get_chapiter_delete_url(self):
        return reverse(
            "course:delete_course_url",
            kwargs={
                "link": str(self.subject.instructor.link),
                "slug": str(self.subject.slug),
                "pk": str(self.pk),
            },
        )

    def get_chapiter_lesson_list_url(self):
        return reverse(
            "course_chapter:chapter_list_url",
            kwargs={
                "link": str(self.subject.instructor.link),
                "slug": str(self.subject.slug),
                "pk": str(self.pk),
            },
        )

    def get_chapiter_lesson_create_url(self):
        return reverse(
            "course_chapter:chapter_create_url",
            kwargs={
                "link": str(self.subject.instructor.link),
                "slug": str(self.subject.slug),
                "pk": str(self.pk),
            },
        )

    @mark_safe
    @admin.display(description="course description")
    def course_description(self):
        return self.description

    # chapitres dans un cours
    def course_lessons(self):
        lessons = CourseChapter.objects.filter(course=self)
        return lessons

    @admin.display(description="lessons", empty_value="???")
    def count_lessons_course(self):
        lessons_count = f"{self.course_lessons().count()}"
        return lessons_count


# Course Chapter : Modules
class CourseChapter(models.Model):
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="chapiter",
        verbose_name="course",
    )
    slug = models.SlugField(
        verbose_name="link of lesson",
        help_text="link of lesson",
        blank=True,
    )
    title = models.CharField(
        verbose_name="lesson title", max_length=200, help_text="add lesson title"
    )
    chapter_desc = models.TextField(
        verbose_name="lesson description",
        blank=True,
        null=True,
        help_text="add lesson description",
    )
    order = func_utils.CustomFields(
        blank=True, verbose_name="lesson number", for_fields=["course"]
    )
    access = models.BooleanField(default=True, verbose_name="lesson is access ?")
    movie = models.URLField(
        verbose_name="url movie", help_text="add movies url", blank=True
    )
    document = models.FileField(
        upload_to=func_utils.save_chapiter_content_file,
        verbose_name="document",
        help_text="upload file",
        blank=True,
    )
    created_at = models.DateField(
        verbose_name="date created",
        auto_now_add=True,
        auto_now=False,
    )
    update_at = models.DateTimeField(
        verbose_name="date updated", auto_now=True, auto_now_add=False
    )

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "lessons"
        indexes = [
            models.Index(fields=["id"]),
        ]

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse(
            "lessons:chapiter_lesson_detail",
            kwargs={
                "slug": str(self.course.subject.slug),
                "chapiter_slug": str(self.course.slug),
                "pk": str(self.course.pk),
                "lesson_slug": str(self.slug),
            },
        )

    def get_lesson_list_url(self):
        return reverse(
            "course_chapter:chapter_list_url",
            kwargs={
                "link": str(self.course.subject.instructor.link),
                "slug": str(self.course.slug),
                "pk": str(self.course.pk),
            },
        )

    def get_lesson_update_url(self):
        return reverse(
            "course_chapter:chapter_update_url",
            kwargs={
                "link": str(self.course.subject.instructor.link),
                "slug": str(self.course.subject.slug),
                "pk": str(self.course.pk),
                "lesson_pk": int(self.pk),
            },
        )


@receiver([models.signals.pre_save], sender=Course)
@receiver([models.signals.pre_save], sender=Subject)
@receiver([models.signals.pre_save], sender=CourseChapter)
def subject_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = func_utils.unique_slug_generator(instance)


@receiver([models.signals.post_save], sender=Course)
def delete_old_image(sender, instance, *args, **kwargs):
    if hasattr(instance, "_current_image"):
        if instance._current_image != instance.image.path:
            instance._current_image.delete(save=False)
