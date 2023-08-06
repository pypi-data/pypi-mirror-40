from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from .serializers import UserCreateSerializer, UserGetSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer