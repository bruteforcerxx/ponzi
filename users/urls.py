from django.urls import path
from .views import ListUsers, Login

urlpatterns = [
    path('users/', ListUsers.as_view()),
    path('login/', Login.as_view())
]
