import uuid

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User, PreUser
from .serializers import UserSerializer, PreUserSerializer


class CurrentUserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            uuid_token = serializer.data['uuid_token']
            raw_password = serializer.data['password']

            pre_user = PreUser.objects.filter(uuid_token=uuid_token).values()

            if raw_password == pre_user[0]['password']:
                User.objects.create(
                                  username=pre_user[0]['username'],
                                  password=make_password(pre_user[0]['password']),
                                  email=pre_user[0]['email'],
                                  first_name=pre_user[0]['first_name'],
                                  last_name=pre_user[0]['last_name'],
                                  middle_name=pre_user[0]['middle_name'],
                                  phone_number=pre_user[0]['phone_number'],
                                  address=pre_user[0]['address'],
                                )

        except IntegrityError:
            # handle a unique login
            content = {'error': 'IntegrityError, please enter other username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class RegisterPreUserView(CreateAPIView):
    queryset = PreUser.objects.all()
    serializer_class = PreUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        uuid_token = uuid.uuid4()
        serializer.save(uuid_token=uuid_token)
