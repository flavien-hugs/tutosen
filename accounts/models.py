# accounts.models.py

import uuid
import random
import string
import phonenumbers

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import Truncator
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

import markdown as md
from allauth.account.models import EmailAddress
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from utils import func_utils
from accounts import managers


def random_digits_generator():
    return "".join(random.choices(string.digits, k=5))


class User(AbstractUser):
    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Élève"
        PARENT_OR_TUTOR = "PARENT_OR_TUTOR", "Parent/Tuteur"
        TEACHER = "TEACHER", "Enseignant(e)/Professionnel(le)"

    base_type = Types.STUDENT

    CIVILITY_CHOICES = (
        ("M.", "M."),
        ("Mme", "Mme"),
        ("Mlle", "Mlle"),
    )

    username = None

    uuid = models.UUIDField(
        db_index=True, default=uuid.uuid4, editable=False, verbose_name="UUID"
    )
    civility = models.CharField(
        max_length=4,
        default="M.",
        choices=CIVILITY_CHOICES,
        verbose_name="civilité",
    )
    type = models.CharField(
        verbose_name="user type",
        max_length=50,
        choices=Types.choices,
        default=base_type,
    )
    email = models.EmailField(
        default="adresseemail@gmail.com",
        max_length=80,
        unique=True,
        verbose_name="adresse email",
    )
    statut = models.CharField(
        max_length=150,
        verbose_name="statut",
        blank=True,
        null=True,
        help_text="Votre statut actuelle.",
    )
    brief_desc = models.TextField(
        verbose_name="brief description",
        blank=True,
        null=True,
        help_text="Vous pour utiliser la syntaxe markdown\
        pour éditer votre profile.",
    )
    phone_number = PhoneNumberField(verbose_name="Téléphone mobile", blank=True)
    state = models.CharField(
        verbose_name="ville de résidence", max_length=120, blank=True, null=True
    )
    country = CountryField(
        blank_label="sélection un pays",
        verbose_name="pays de résidence",
        multiple=False,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name="user avatar",
        null=True,
        blank=True,
        upload_to=func_utils.save_avatar_file,
    )
    cover = models.ImageField(
        verbose_name="user cover",
        blank=True,
        null=True,
        upload_to=func_utils.save_cover_file,
    )
    link = models.SlugField(
        unique=True, editable=False, max_length=225, blank=True, null=True
    )

    facebook = models.CharField(
        verbose_name="compte facebook", max_length=250, blank=True, null=True
    )
    twitter = models.CharField(
        verbose_name="compte twitter", max_length=250, blank=True, null=True
    )
    linkedin = models.URLField(
        verbose_name="compte linkedin", max_length=250, blank=True, null=True
    )

    objects = managers.UserManager()
    teachers = managers.TeacherManager()
    students = managers.StudentManager()
    tutors = managers.ParentOrTutorManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined", "-last_login")
        get_latest_by = ("-date_joined", "-last_login")
        verbose_name_plural = "Utilisateurs"
        indexes = [models.Index(fields=["id", "uuid"])]

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = random_digits_generator()

        if not self.type:
            self.type = self.base_type

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_fullname()}"

    def formatted_phone(self, country=None):
        return phonenumbers.parse(self.phone_number, country)

    @mark_safe
    @admin.display(ordering="type", empty_value="???", description="statut")
    def colored_type(self):
        if self.type == "TEACHER":
            color = "754ff6"
        elif self.type == "STUDENT":
            color = "18113c"
        else:
            color = "19cb98"
        render_color = format_html(
            f"""
            <span style='color:#fff; background-color:#{color};\
            display:inline-block; font-weight:500; write-space:nowrap;\
            line-height:1;border-radius:.20rem; padding:.33rem .5rem;\
            text-align:center;vertical-align:baseline;text-transform:uppercase;'>
            {self.get_type_display()}
            </span>"""
        )
        return render_color

    @admin.display(description="nom & prénom")
    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    @admin.display(description="speudo")
    def get_speudonyme(self):
        return f"@{self.username.lower()}"

    @admin.display(description="user description")
    def get_description(self):
        truncated_desc = Truncator(str(self.brief_desc))
        truncated_desc_chars = truncated_desc.chars(30)
        return truncated_desc_chars

    @admin.display(description="account verified")
    def account_verified(self):
        result = EmailAddress.objects.filter(email=self.email)
        if len(result):
            return result[0].verified
        return False

    def get_description_as_markdown(self):
        markdown_render = md.markdown(
            self.brief_desc or "", extensions=["markdown.extensions.fenced_code"]
        )
        return markdown_render

    def get_first_name(self):
        return f"{self.first_name}".replace(" ", "-").lower()

    def get_userdetail_url(self):
        path = ""
        if self.type == "TEACHER":
            path = reverse("boards:teacher_detail", kwargs={"link": str(self.link)})
        elif self.type == "STUDENT":
            path = reverse("boards:student_detail", kwargs={"link": str(self.link)})
        return path

    def get_userupdate_url(self):
        return reverse("boards:teacher_update", kwargs={"link": str(self.link)})

    def get_userdelete_url(self):
        return reverse("boards:teacher_delete", kwargs={"link": str(self.link)})

    def get_teacher_detail_url(self):
        return reverse("accounts:teacher_detail_view", kwargs={"link": self.link})

    def get_teacher_course_url(self):
        return reverse("accounts:teacher_course_url", kwargs={"link": self.link})

    def get_teacher_post_url(self):
        return reverse("accounts:teacher_blog_url", kwargs={"link": self.link})

    def get_teacher_courses(self):
        from courses.models import Subject

        courses = Subject.objects.get_courses_published().filter(instructor=self)
        return courses

    @admin.display(description="numbers of course")
    def get_teacher_courses_count(self):
        number_of_courses = self.get_teacher_courses().aggregate(
            count=models.Count("id")
        )
        counter = 0
        if number_of_courses["count"] is not None:
            counter = int(number_of_courses["count"])
        return counter

    @admin.display(description="posts", empty_value="???")
    def get_posts(self):
        from blog.models import Post

        posts = Post.objects.published().filter(author=self)
        return posts

    def get_posts_last_count(self):
        posts_count_last = (
            self.get_posts()
            .filter(created_at__lte=timezone.now())
            .aggregate(count=models.Count("id"))
        )
        counter = 0
        if posts_count_last["count"] is not None:
            counter = int(posts_count_last["count"])
        return counter

    @admin.display(description="number of posts", empty_value="???")
    def get_posts_count(self):
        posts_count = self.get_posts().aggregate(count=models.Count("id"))
        counter = 0
        if posts_count["count"] is not None:
            counter = int(posts_count["count"])
        return counter

    def get_local_today(self):
        # recupere la date de l'User conneceté en cours
        return timezone.now()


class Teacher(User):
    base_type = User.Types.TEACHER

    class Meta:
        proxy = True
        ordering = ("-date_joined", "-last_login")
        get_latest_by = ("-date_joined", "-last_login")
        verbose_name_plural = "instructeurs"

    def email_name(self):
        email_address = self.email.split("@")[0]
        return email_address

    def sign_in(self, request):
        request.session["email"] = self
        self.date_joined = timezone.now()
        self.save()

    def sign_out(self):
        if "email" in self.request.session:
            del self.request.session["email"]

    def get_signed_in(self):
        if "email" in self.request.session:
            return self.request.session["email"]
        return None


class Student(User):
    base_type = User.Types.STUDENT

    class Meta:
        proxy = True
        ordering = ("-date_joined", "-last_login")
        get_latest_by = ("-date_joined", "-last_login")
        verbose_name_plural = "Etudiants(es)"


class ParentOrTutor(User):
    base_type = User.Types.PARENT_OR_TUTOR

    class Meta:
        proxy = True
        ordering = ("-date_joined", "-last_login")
        get_latest_by = ("-date_joined", "-last_login")
        verbose_name_plural = "tuteurs/trices"


@receiver([models.signals.post_save], sender=Student)
@receiver([models.signals.post_save], sender=Teacher)
@receiver([models.signals.post_save], sender=ParentOrTutor)
def user_post_save_receiver(sender, instance, **kwargs):
    User.objects.filter(email=instance)


@receiver([models.signals.post_save], sender=Student)
@receiver([models.signals.post_save], sender=Teacher)
@receiver([models.signals.post_save], sender=ParentOrTutor)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_image = User.objects.get(pk=instance.pk).cover
            if old_image and old_image.url != instance.cover.url:
                old_image.delete(save=False)
        except:
            pass
