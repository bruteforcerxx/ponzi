from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView 
from .models import Transaction
from users.models import User
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Create your views here.
class ListCreateTransactions(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.data['by'])
        serializer.save(by=user)

# class CoinbaseNotification(APIView):
#     def get(self, request):
#         print(request)
#         return Response({'hey': 'hey'})
    
#     def post(self, request, format=None):
#         print(request)

class TransactionCreate(APIView):
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        return Response({'method': request.data})

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

class TransactionDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserTransactions(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    def get_queryset(self):
        user_id = self.request.GET.get('user_id', '')
        user = User.objects.get(id=user_id)
        queryset = Transaction.objects.filter(by=user)
        return queryset
    
    
    def handle_exception(self, exc):
        return Response({'error': str(exc)})