# api.views.py

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import pagination
from api.serializers import UserSerializer
from api.permissions import IsUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsUserOrReadOnly]
    pagination_class = pagination.LimitOffsetPagination

user_view_set = UserViewSet
