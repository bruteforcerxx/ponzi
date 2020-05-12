from django.urls import path
from .views import UserDebitTransactions, UserCreditTransactions, ListCreateTransactions, CoinbaseNotification, TransactionDetails, UserTransactions

urlpatterns = [
    path('transactions/', ListCreateTransactions.as_view()),
    path('transactions/<int:pk>/', TransactionDetails.as_view()),
    path('transactions/user/', UserTransactions.as_view()),
    path('transactions/user/credits/', UserCreditTransactions.as_view()),
    path('transactions/user/debits/', UserDebitTransactions.as_view()),
    path('coinbase/', CoinbaseNotification)
]
