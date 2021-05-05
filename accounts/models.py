# accounts.models.py

import uuid
from django.db import models
from django.urls import reverse
from django.db.models import Index
from allauth.account.models import EmailAddress
from django.db.models.functions import Lower, Upper
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from accounts import managers


class User(AbstractUser):

    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Intructeur(trice)"
        STUDENT = "STUDENT", "Etudiant(e)"

    base_type = Types.STUDENT

    CIVILITY_CHOICES = (
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('Mlle', 'Mlle'),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
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
    avatar = models.ImageField(
        verbose_name='photo de profile',
        upload_to='image/',
        null=True, blank=True
    )
    brief_desc = RichTextField(
        verbose_name='brief description',
        blank=True, null=True
    )
    phone_number = PhoneNumberField(
        verbose_name='téléphone',
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
        multiple=False,
        blank=True
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
        verbose_name_plural = 'Utilisateur'

        indexes = [
            Index(
                Lower('first_name'),
                Upper('last_name').desc(),
                name='first_last_name_idx'
            ),
            models.Index(fields=['id'], name='id_index'),
        ]

    def _get_unique_username(self):
        if self.username:
            username = str(self.username)
        else:
            username = "tutosen"
        unique_username = username

        if User.objects.filter(username=unique_username).exists():
            unique_username = "{0}".format(username)
        return unique_username

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        self.username = self._get_unique_username()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.get_fullname())

    def get_fullname(self):
        return '{0} {1} {2}'.format(
            self.get_civility_display(),
            self.first_name,
            self.last_name
        )
    get_fullname.short_description = 'Nom & prénom'

    def get_speudonyme(self):
        return '@{0}'.format(
            self.username.lower(),
        )
    get_speudonyme.short_description = 'Speudo'

    def get_description(self):
        if len(self.brief_desc) > 30:
            return '{0} {1}'.format(self.brief_desc[:29], '...')
        else:
            return self.brief_desc
    get_description.short_description = 'Description'

    def get_userdetail_url(self):
        return reverse(
            'boards:user_detail',
            kwargs={'pk': str(self.uuid)}
        )

    def get_userupdate_url(self):
        return reverse(
            'boards:user_update',
            kwargs={'pk': str(self.uuid)}
        )

    def get_userdelete_url(self):
        return reverse(
            'boards:user_delete',
            kwargs={'pk': str(self.uuid)}
        )

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.email)
            if len(result):
                return result[0].verified
            return False


class Teacher(User):
    base_type = User.Types.TEACHER

    USERNAME_FIELD = 'first_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = managers.TeacherManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Intructeur(trice)'

    def get_teacher_detail_url(self):
        return reverse(
            'accounts:teacher_detail_view',
            kwargs={
                'username': str(self.first_name.lower().replace(" ", "-")),
                'pk': str(self.id)
            }
        )


class Student(User):
    base_type = User.Types.STUDENT

    USERNAME_FIELD = 'first_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = managers.StudentManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Etudiant(e)'

    def more(self):
        return self.studentmore
    more.short_description = "Qui suis-je ?"


# from django.dispatch import receiver
# from django.db.models.signals import post_save


# @receiver(post_save, sender=TeacherMore)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         TeacherMore.objects.create(user=instance)

# @receiver(post_save, sender=TeacherMore)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
