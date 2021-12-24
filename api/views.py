# api.views.py

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import pagination
from api import serializers, permissions

from courses import models


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsUserOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination


user_viewset = UserViewSet


class CourseViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    queryset = models.Subject.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsUserOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination


course_viewset = CourseViewSet