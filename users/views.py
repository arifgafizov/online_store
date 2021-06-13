from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


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
            raw_password = new_user.password
            new_user.set_password(raw_password)
            new_user.save()
