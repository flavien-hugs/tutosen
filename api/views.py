# api.views.py

from django.contrib.auth import get_user_model

from api.serializers import UserSerializer
from api.permissions import IsUserOrReadOnly
from rest_framework import generics, permissions


class UserListAPIView(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


user_list_api_view = UserListAPIView.as_view()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsUserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = get_user_model().objects.all()


user_detail_api_view = UserDetailAPIView.as_view()
