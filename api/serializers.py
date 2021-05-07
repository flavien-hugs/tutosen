# api.serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'uuid', 'last_name', 'first_name',
            'username', 'phone_number', 'email', 'type', 'statut',
            'state', 'country', 'facebook', 'twitter', 'linkedin',
            'date_joined', 'last_login'
        ]
        depth = 2


# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['__all__']
