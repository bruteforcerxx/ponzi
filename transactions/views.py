from django.shortcuts import render
from rest_framework import generics 
from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class ListCreateTransactions(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer