import uuid
from datetime import datetime

from django.contrib.auth.hashers import make_password
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uuid_token = serializer.data['uuid_token']
        raw_password = serializer.data['password']
        valid_timedelta = datetime.now() - settings.TIMEDELTA

        # geting the preuser that has not expired in the Preuser table
        try:
            pre_user = PreUser.objects.get(uuid_token=uuid_token, created_at__gte=valid_timedelta)
        except PreUser.DoesNotExist:
            raise ValidationError({"expired": "Token not exist or expired."})

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

        headers = self.get_success_headers(serializer.data)
        # generating authorization token and serializing user to send
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = CurrentUserSerializer(user)

        return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class RegisterPreUserView(CreateAPIView):
    queryset = PreUser.objects.all()
    serializer_class = PreUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        valid_timedelta = datetime.now() - settings.TIMEDELTA

        # checking the unique username in the User table
        if User.objects.filter(username=username).exists():
            raise ValidationError({"unique": "A user with that username already exists."})
        else:
            # checking the unique username that has not expired in the Preuser table
            if PreUser.objects.filter(username=username,
                                      created_at__gte=valid_timedelta).exists():
                raise ValidationError({"unique": "this username is already reserved."})

        # checking the unique email in the User table
        if User.objects.filter(email=email).exists():
            raise ValidationError({"unique": "A user with that email already exists."})
        else:
            # checking the unique email that has not expired in the Preuser table
            if PreUser.objects.filter(email=email,
                                      created_at__gte=valid_timedelta).exists():
                raise ValidationError({"unique": "this email is already reserved."})

        uuid_token = uuid.uuid4()
        serializer.save(uuid_token=uuid_token)
