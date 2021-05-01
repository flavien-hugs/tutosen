# accounts.models.py

import hashlib
from django.db import models
from django.urls import reverse
from django.db.models import Index
from allauth.account.models import EmailAddress
from django.db.models.functions import Lower, Upper
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount

from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# from accounts import managers


class User(AbstractUser):

    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    base_type = Types.TEACHER

    CIVILITY_CHOICES = (
        ('M.', 'M.'),
        ('Mme', 'Mme'),
        ('Mlle', 'Mlle'),
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

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.first_name)
 
    class Meta:        
        db_table = 'user_profile'
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Utilisateur'

        indexes = [
            Index(Lower('first_name'), Upper('last_name').desc(), name='first_last_name_idx'),
            models.Index(fields=['id'], name='id_index'),
        ]

    def get_fullname(self):
        return '{0} {1} {2}'.format(
            self.civility,
            self.first_name,
            self.last_name
        )
    get_fullname.short_description = 'Nom & prénom'

    def get_speudonyme(self):
        return '@{0}'.format(
            self.first_name.lower(),
        )

    def get_userdetail_url(self):
        return reverse(
            'boards:user_detail',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'pk': str(self.id),
            }
        )

    def get_userupdate_url(self):
        return reverse(
            'boards:user_update',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'pk': str(self.id),
            }
        )

    def get_userdelete_url(self):
        return reverse(
            'boards:user_delete',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'pk': str(self.id),
            }
        )

    def get_social_profile_update_url(self):
        return reverse(
            'boards:social_account_update',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'pk': str(self.id),
            }
        )
 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


class TeacherManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        is_teacher = User.Types.TEACHER
        return super().get_queryset(*args, **kwargs).filter(type=is_teacher)


class StudentManager(models.Manager):
    
    def get_queryset(self, *args, **kwargs):
        is_student = User.Types.STUDENT
        return super().get_queryset(*args, **kwargs).filter(type=is_student)


class TeacherMore(models.Model):
    user = models.OneToOneField(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name='instructeur'
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
    qualification = RichTextField(
        verbose_name='qualification',
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
        max_length=250,
        blank=True, null=True
    )
    twitter = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    linkedin = models.CharField(
        max_length=250,
        blank=True, null=True
    )

    class Meta:
        verbose_name_plural = 'Intructeur detail'

    def __str__(self):
        return '{0}'.format(self.user.first_name)


class Teacher(User):
    base_type = User.Types.TEACHER

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = TeacherManager()

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Intructeur'

    def get_teacher_detail_url(self):
        return reverse(
            'accounts:teacher_detail_view',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'pk': str(self.id),
            }
        )

    def whisper(self):
        return "chuchoter"


class StudentMore(models.Model):
    user = models.OneToOneField(
        'Student',
        verbose_name='etudiant',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Etudiant detail'


class Student(User):
    base_type = User.Types.STUDENT

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = StudentManager()

    def more(self):
        return self.studentmore
    more.short_description = "Qui suis-je ?"

    class Meta:
        proxy = True
        ordering = ('-date_joined', '-last_login')
        get_latest_by = ('-date_joined', '-last_login')
        verbose_name_plural = 'Etudiant'

    def accelerate(self):
        return "Aller plus vite"
