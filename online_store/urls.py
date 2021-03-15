"""online_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='Online store DRF API',
        default_version='v1',

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.TokenAuthentication,),
)

api_urlpatterns = [
    path('', include(('products.urls', 'products'), namespace='products')),
    path('users/', include('users.urls')),
    path('', include('carts.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]