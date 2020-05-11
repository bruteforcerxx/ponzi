from django.urls import path
from .views import ListCreateTransactions

urlpatterns = [
    path('transactions/', ListCreateTransactions.as_view())
]
