# accounts.models.py

import uuid
import time
import datetime

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import Truncator
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models.functions import Lower, Upper
from django.contrib.auth.models import AbstractUser

import markdown as md
from allauth.account.models import EmailAddress
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from utils import func_utils
from accounts import managers


class User(AbstractUser):

    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Élève"
        PARENT_OR_TUTOR = "PARENT_OR_TUTOR", "Parent/Tuteur"
        TEACHER = "TEACHER", "Enseignant(e)/Professionnel(le)"

    base_type = Types.STUDENT

    CIVILITY_CHOICES = (
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('Mlle', 'Mlle'),
    )

    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID'
    )
    civility = models.CharField(
        max_length=4,
        default="M.",
        choices=CIVILITY_CHOICES,
        verbose_name='civilité',
    )
    type = models.CharField(
        verbose_name='statut',
        max_length=50,
        choices=Types.choices,
        default=base_type
    )
    statut = models.CharField(
        max_length=150,
        verbose_name='statut',
        blank=True, null=True,
        help_text='Votre statut actuelle.'
    )
    brief_desc = models.TextField(
        verbose_name='brief description',
        blank=True, null=True,
        help_text='Vous pour utiliser la syntaxe markdown\
        pour éditer votre profile.'
    )
    phone_number = PhoneNumberField(
        verbose_name='Téléphone mobile',
        blank=True
    )
    state = models.CharField(
        verbose_name='ville de résidence',
        max_length=120,
        blank=True, null=True
    )
    country = CountryField(
        blank_label='sélection un pays',
        verbose_name='pays de résidence',
        multiple=False, blank=True
    )
    avatar = models.ImageField(
        verbose_name='user avatar',
        null=True, blank=True,
        upload_to=func_utils.save_user_avatar_file
    )
    cover = models.ImageField(
        verbose_name="user cover",
        blank=True, null=True,
        upload_to=func_utils.save_user_cover_file
    )
    facebook = models.CharField(
        verbose_name='compte facebook',
        max_length=250,
        blank=True, null=True
    )
    twitter = models.CharField(
        verbose_name='compte twitter',
        max_length=250,
        blank=True, null=True
    )
    linkedin = models.URLField(
        verbose_name='compte linkedin',
        max_length=250,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'user_profile'
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Utilisateurs'
        indexes = [
            models.Index(fields=['id', 'uuid'], name='id_index_user'),
        ]

    def _get_unique_username(self):
        if self.username:
            username = str(self.username)
        else:
            username = str(self.email)
        self.username = username

        if User.objects.filter(username=username).exists():
            username = self.email
        return username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type

        if self.username:
            self.username = self._get_unique_username()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_fullname()}"

    @mark_safe
    @admin.display(ordering='type', empty_value='???', description='statut')
    def colored_type(self):
        if self.type == 'TEACHER':
            color = "754ff6"
        elif self.type == 'STUDENT':
            color = "18113c"
        else:
            color = "19cb98"
        render_color = format_html(
            f"<span style='color:#fff; background-color:#{color};\
            display:inline-block; font-weight:500; write-space:nowrap;\
            line-height:1;border-radius:.20rem; padding:.33rem .5rem;\
            text-align:center;vertical-align:baseline;'>{self.get_type_display()}</span>"
        )
        return render_color

    @admin.display(description="nom & prénom")
    def get_fullname(self):
        return f"{self.get_civility_display()} {self.first_name} {self.last_name}"

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
            self.brief_desc or u'',
            extensions=['markdown.extensions.fenced_code']
        )
        return markdown_render

    def get_first_name(self):
        return f"{self.first_name}".replace(' ', '.').lower()

    def get_userdetail_url(self):
        path = ""
        if self.type == 'TEACHER':
            path = reverse(
                'boards:teacher_detail',
                kwargs={'username': str(self.get_first_name())}
            )
        elif self.type == 'STUDENT':
            path = reverse(
                'boards:student_detail',
                kwargs={'username': str(self.get_first_name())}
            )
        return path

    def get_userupdate_url(self):
        return reverse(
            'boards:teacher_update',
            kwargs={'username': str(self.get_first_name())}
        )

    def get_userdelete_url(self):
        return reverse(
            'boards:teacher_delete',
            kwargs={'username': str(self.get_first_name())}
        )

    def get_teacher_detail_url(self):
        return reverse(
            'accounts:teacher_detail_view',
            kwargs={'uuid': self.uuid}
        )

    def get_teacher_courses(self):
        from courses.models import Subject
        courses = Subject.objects.get_courses_published().filter(published=True)
        return courses

    def get_teacher_courses_count(self):
        number_of_courses = self.get_teacher_courses().count()
        return number_of_courses

    # def get_local_today(self):
    #     # recupere la date de l'User conneceté
    #     # en cours
    #     return datetime.timezone.localedate()


class Teacher(User):
    base_type = User.Types.TEACHER

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = managers.TeacherManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Enseignant(e) ou professionnel(le)'

    def email_name(self):
        email_address = self.email.split('@')[0]
        return email_address

    def sign_in(self, request):
        request.session['email'] = self
        self.date_joined = datetime.datetime.now()
        self.save()

    def sign_out(self):
        if 'email' in self.request.session:
            del self.request.session['email']

    def get_signed_in(cls, request):
        if 'email' in request.session:
            return request.session['email']
        else:
            return None


class Student(User):
    base_type = User.Types.STUDENT

    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = managers.StudentManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Etudiant(e)'


class ParentOrTutor(User):
    base_type = User.Types.PARENT_OR_TUTOR

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'first_name'
    REQUIRED_FIELDS = ['email']

    objects = managers.ParentOrTutorManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Etudiant(e)'


@receiver([models.signals.post_save], sender=Student)
@receiver([models.signals.post_save], sender=Teacher)
@receiver([models.signals.post_save], sender=ParentOrTutor)
def user_post_save_receiver(sender, instance, **kwargs):
    User.objects.filter(username=instance)


@receiver([models.signals.post_save], sender=Student)
@receiver([models.signals.post_save], sender=Teacher)
@receiver([models.signals.post_save], sender=ParentOrTutor)
def delete_old_image(sender, instance, *args, **kwargs):
    if hasattr(instance, '_current_cover_file'):
        if instance._current_cover_file != instance.cover.path:
            instance._current_cover_file.delete(save=False)
