from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView 
from .models import Transaction
from users.models import User
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal
from rest_framework import status
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from coinbase.wallet.client import Client
import os
import time
import json
from dotenv import load_dotenv
import requests
from threading import Thread
from .funding_manager_luno import funding_manager_luno 
load_dotenv()
from .send_to_luno import send_to_luno

# Create your views here.
class ListCreateTransactions(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.data['by'])
        type = self.request.data['type']
        amount = Decimal(self.request.data['amount'])
        if type == 'credit':
            user.balance += amount
        elif type == 'debit':
            # transaction type is debit
            if Decimal(user.balance) < amount:
                raise ValidationError({'error': 'Insufficient funds'})
            user.balance -= amount
        user.save()
        serializer.save(by=user)

# class CoinbaseNotification(APIView):
#     def get(self, request):
#         print(request)
#         return Response({'hey': 'hey'})
    
#     def post(self, request, format=None):
#         print(request)


class TransactionDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns a transaction's details, updates and deletes it
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserTransactions(generics.ListAPIView):
    """
    Returns all transactions, debit and credit, performed by user
    """
    serializer_class = TransactionSerializer
    def get_queryset(self):
        user_id = self.request.GET.get('user_id', '')
        user = User.objects.get(id=user_id)
        queryset = Transaction.objects.filter(by=user)
        return queryset
    

    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class UserCreditTransactions(generics.ListAPIView):
    """
    Returns all credit transaction done by user
    """
    serializer_class = TransactionSerializer
    def get_queryset(self):
        user_id = self.request.GET.get('user_id', '')
        user = User.objects.get(id=user_id)
        queryset = Transaction.objects.filter(by=user, type='credit')
        return queryset
        
    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class UserDebitTransactions(generics.ListAPIView):
    """
    Returns all debit transaction done by user
    """
    serializer_class = TransactionSerializer
    def get_queryset(self):
        user_id = self.request.GET.get('user_id', '')
        user = User.objects.get(id=user_id)
        queryset = Transaction.objects.filter(by=user, type='debit')
        return queryset
        
    def handle_exception(self, exc):
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def CoinbaseNotification(request):
    """
    Retrieve, update or delete a code snippet.
    """

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
                    return Response({'error': 'currency is not BTC'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Sending user not found'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def CoinbaseWalletCreate(request):
    """
    Endpoint for creating wallet address for user to deposit bitcoin to
    """
    
    for_user = request.POST.get('user_id', '') #get id for user who should own the wallet address
    if for_user == '':
        return Response({'error': 'user_id missing in request data'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id = for_user)
        get_id = open('jsons/coinbase_funded_keys.json', 'r')
        id = json.load(get_id)
        get_id.close()

        use_id = id[0]
        secret = use_id[0]
        cb_key = use_id[1]
        cb_id = use_id[2]

        client = Client(cb_key, secret)
        try:
            address = client.create_address(cb_id)['address'] #get address value of newly created address
            user.to_wallet = address

            pending = open('jsons/addresses.json', 'r')
            public_ads = json.load(pending)
            pending.close()
            for element in public_ads:
                if element[1] == user.email:
                    print(element)
                    del(public_ads[public_ads.index(element)])

            public_ads.append([address, user.email])

            pending = open('jsons/addresses.json', 'w')
            json.dump(public_ads, pending)
            pending.close()
            user.save()
            return Response({
            'user':{
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'to_wallet': user.to_wallet,
                'balance': user.balance
            },
            'address': address
        }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_408_REQUEST_TIMEOUT)
    except User.DoesNotExist:
        return Response({'error': 'User with given id "%s" does not exist' % for_user}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def GetCoinbaseNotifications(request):
    API_KEY = os.environ['COINBASE_API_KEY']
    API_SECRET = os.environ['COINBASE_API_SERCRET']
    ACCOUNT_ID = os.environ['COINBASE_ACCOUNT_ID']
    client = Client(API_KEY, API_SECRET)
    notifications = client.get_transactions(ACCOUNT_ID)
    return Response(notifications, status=status.HTTP_200_OK)


@api_view(['POST'])
def WIthdrawToLuno(request):
    for_user = request.POST.get('user_id', '')
    amount = request.POST.get('amount', '')
    address = request.POST.get('address', '')

    send_to_luno(for_user, amount, address, '')
    return Response({'data': 'Transaction complete'}, status=status.HTTP_200_OK)



