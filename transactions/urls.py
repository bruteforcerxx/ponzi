from django.urls import path
from .views import (UserDebitTransactions, CoinbaseWalletCreate,
UserCreditTransactions, ListCreateTransactions, GetCoinbaseNotifications,
CoinbaseNotification, TransactionDetails, UserTransactions, WIthdrawToLuno)

urlpatterns = [
    path('transactions/', ListCreateTransactions.as_view()),
    path('transactions/<int:pk>/', TransactionDetails.as_view()),
    path('transactions/user/', UserTransactions.as_view()),
    path('transactions/user/credits/', UserCreditTransactions.as_view()),
    path('transactions/user/debits/', UserDebitTransactions.as_view()),
    path('coinbase_notifications/', CoinbaseNotification),
    path('wallet_create/', CoinbaseWalletCreate),
    path('notifications_list/', GetCoinbaseNotifications),
    path('withdraw_to_luno/', WIthdrawToLuno)
]
