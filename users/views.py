import uuid

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
            new_user = serializer.save()
        except IntegrityError:
            # handle a unique login
            content = {'error': 'IntegrityError, please enter other username'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            pre_user = PreUser.objects.filter(uuid_token=new_user.uuid_token)
            raw_password = new_user.password
            new_user.set_password(raw_password)
            new_user.save(
                          username=pre_user.username,
                          email=pre_user.email,
                          first_name=pre_user.first_name,
                          last_name=pre_user.last_name,
                          middle_name=pre_user.middle_name,
                          phone_number=pre_user.phone_number,
                          address=pre_user.address,
                        )


class RegisterPreUserView(CreateAPIView):
    queryset = PreUser.objects.all()
    serializer_class = PreUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        uuid_token = uuid.uuid4()
        serializer.save(uuid_token=uuid_token)
