from django.urls import path

from search.views import SearchProducts

urlpatterns = [
    path('product/<str:query>/', SearchProducts.as_view()),
]
