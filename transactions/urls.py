from django.urls import path
from .views import ListCreateTransactions, CoinbaseNotification

urlpatterns = [
    path('transactions/', ListCreateTransactions.as_view()),
    path('coinbase/', CoinbaseNotification)
]
