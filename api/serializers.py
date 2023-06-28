# api.serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin

from courses.models import Subject


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "uuid",
            "last_name",
            "first_name",
            "username",
            "phone_number",
            "email",
            "type",
            "statut",
            "state",
            "country",
            "facebook",
            "twitter",
            "linkedin",
            "date_joined",
            "last_login",
        ]
        depth = 1


class CourseSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "pk",
            "uuid",
            "title",
            "subtitle",
            "price",
            "sale_price",
            "language",
            "category",
            "level",
            "description",
            "resume",
            "free",
            "published",
            "slug",
            "image",
            "created_at",
            "update_at",
        ]
        depth = 1
