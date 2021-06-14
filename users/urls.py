from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users.views import RegisterPreUserView, CurrentUserRetrieveUpdateView

urlpatterns = [
    path('auth/login/',  obtain_auth_token),
    path('auth/register/', RegisterPreUserView.as_view(), name='register'),
    path('auth/current/', CurrentUserRetrieveUpdateView.as_view(), name='current'),
]
