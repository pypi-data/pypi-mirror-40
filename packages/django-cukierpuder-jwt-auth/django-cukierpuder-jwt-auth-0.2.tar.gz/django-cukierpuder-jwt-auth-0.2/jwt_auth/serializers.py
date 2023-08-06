from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ReadOnlyField
)


class UserCreateSerializer(ModelSerializer):
    email = EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )


class UserGetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )