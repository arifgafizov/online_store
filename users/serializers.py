from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User, PreUser


class UserSerializer(ModelSerializer):
    uuid_token = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'uuid_token',
        ]


class PreUserSerializer(ModelSerializer):

    class Meta:
        model = PreUser
        fields = [
            'id',
            'username',
            'password',
            'uuid_token',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'address',
        ]
