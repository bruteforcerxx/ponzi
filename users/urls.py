from django.urls import path, include
from .views import ListUsers

urlpatterns = [
    path('users/', ListUsers.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
