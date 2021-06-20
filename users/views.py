import uuid
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from .models import User, PreUser
from .serializers import PreUserSerializer, CurrentUserSerializer, RegisterUserSerializer


class CurrentUserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            uuid_token = serializer.data['uuid_token']
            raw_password = serializer.data['password']
            pre_user = PreUser.objects.get(uuid_token=uuid_token)
            valid_timedelta = datetime.now() - settings.TIMEDELTA

            # checking the unique username in the User table
            if User.objects.filter(username=pre_user.username).exists():
                raise ValidationError({"unique": "A user with that username already exists."})
            else:
                # checking the unique username that has not expired, except for the current preuser in the Preuser table
                if PreUser.objects.filter(~Q(uuid_token=uuid_token), username=pre_user.username, created_at__gte=valid_timedelta).exists():
                    raise ValidationError({"unique": "this username is already reserved."})
                else:
                    user = User.objects.create(
                                      username=pre_user.username,
                                      password=make_password(raw_password),
                                      email=pre_user.email,
                                      first_name=pre_user.first_name,
                                      last_name=pre_user.last_name,
                                      middle_name=pre_user.middle_name,
                                      phone_number=pre_user.phone_number,
                                      address=pre_user.address,
                                    )

                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                    # return Response(data={'reason': "invalid password"}, status=status.HTTP_400_BAD_REQUEST)

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
