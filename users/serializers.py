from rest_framework.serializers import ModelSerializer

from .models import User, PreUser


class UserSerializer(ModelSerializer):

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
