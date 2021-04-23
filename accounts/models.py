# accounts.models.py

import uuid
import hashlib
from django.db import models
from django.urls import reverse
from django.db.models import Index
from allauth.account.models import EmailAddress
from django.db.models.functions import Lower, Upper
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount

from accounts.managers import TeacherManager, StudentManager


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
            Index(
                Lower('first_name'),
                Upper('last_name').desc(),
                name='first_last_name_idx',
            )
        ]

    def get_userdetail_url(self):
        return reverse(
            'boards:user_detail',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'id': str(self.id),
            }
        )

    def get_userupdate_url(self):
        return reverse(
            'boards:user_update',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'id': str(self.id),
            }
        )

    def get_userdelete_url(self):
        return reverse(
            'boards:user_delete',
            kwargs={
                'first_name': str(self.first_name.lower()),
                'id': str(self.id),
            }
        )

 
    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

#     def profile_image_url(self):
#         fb_uid = SocialAccount.objects.filter(
#             user_id=self.user.id,
#             provider='facebook'
#         )
        
#         if len(fb_uid):
#             return "http://graph.facebook.com/{0}/picture?width=40&height=40".format(fb_uid[0].uid)

#         return "http://www.gravatar.com/avatar/{0}?s=40".format(hashlib.md5(self.user.email).hexdigest())

# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[:0])


class TeacherMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gadgets = models.TextField()


class Teacher(User):
    base_type = User.Types.TEACHER

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = TeacherManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "chuchoter"


class StudentMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()


class Student(User):
    base_type = User.Types.STUDENT

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = StudentManager()

    @property
    def more(self):
        return self.drivermore

    class Meta:
        proxy = True

    def accelerate(self):
        return "Aller plus vite"
