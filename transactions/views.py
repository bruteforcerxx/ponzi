from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView 
from .models import Transaction
from users.models import User
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal
from rest_framework.status import HTTP_200_OK

# Create your views here.
class ListCreateTransactions(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# class CoinbaseNotification(APIView):
#     def get(self, request):
#         print(request)
#         return Response({'hey': 'hey'})
    
#     def post(self, request, format=None):
#         print(request)
@api_view(['GET', 'POST'])
def CoinbaseNotification(request):
    """
    Retrieve, update or delete a code snippet.
    """
    # try:
    #     snippet = Snippet.objects.get(pk=pk)
    # except Snippet.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # serializer = SnippetSerializer(snippet)
        print(request.method)
        return Response({'hey': 'get'})

    if request.method == 'POST':
        request_type = request.data['type']
        if request_type == 'wallet:deposit:completed':
            try:
                user = User.objects.get(to_wallet = request.data['data']['address'])
                amount = request.data['additional_data']['amount']['amount']
                currency = request.data['additional_data']['amount']['currency']
                hash = request.data['additional_data']['hash']
                if (currency == 'BTC'):
                    user.balance += Decimal(amount)
                    transaction = Transaction()
                    transaction.by = user
                    transaction.tx_hash = hash
                    transaction.amount = Decimal(amount)
                    transaction.summary = 'deposit'
                    transaction.type = 'credit'
                    transaction.description = "Deposit of %d %s made into %s's (%s) account" % (Decimal(amount), currency, user.username, user.email)
                    transaction.status = 'complete'

                    user.save()
                    transaction.save()
                else:
                    return Response({'error': 'currency is not BTC'}, status=HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Sending user not found'}, status=HTTP_200_OK)
        return Response(status=HTTP_200_OK)
