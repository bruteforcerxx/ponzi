from django.urls import path
from .views import TransactionCreate, ListCreateTransactions, CoinbaseNotification, TransactionDetails, UserTransactions

urlpatterns = [
    path('transactions/', ListCreateTransactions.as_view()),
    path('transactions/<int:pk>/', TransactionDetails.as_view()),
    path('transactions/user/', UserTransactions.as_view()),
    path('transactions/create/', TransactionCreate.as_view()),
    path('coinbase/', CoinbaseNotification)
]
