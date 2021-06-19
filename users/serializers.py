from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import User, PreUser


class RegisterUserSerializer(Serializer):
    uuid_token = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class PreUserSerializer(ModelSerializer):

    class Meta:
        model = PreUser
        fields = [
            'id',
            'username',
            'uuid_token',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'address',
        ]


class CurrentUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'address',
        ]


class RegisteredCompleteUserSerializer(Serializer):
    auth_token = serializers.CharField(max_length=128)
    user = CurrentUserSerializer()
