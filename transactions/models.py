from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.
STATUS_CHOICES = [
    ('pending', 'pending'),
    ('complete', 'successful'),
    ('failed', 'failed')
]

TYPE_CHOICES = [
    ('debit', 'debit'),
    ('credit', 'credit')
]

SUMMARY_CHOICES = [
    ('transfer', 'transfer'),
    ('deposit', 'deposit'),
    ('withdrawal', 'withdrawal')
]

class Transaction(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default = timezone.now)
    tx_hash = models.CharField(max_length=400, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=8)
    type = models.CharField(max_length=250, choices=TYPE_CHOICES)
    summary = models.CharField(max_length=250, choices=SUMMARY_CHOICES)
    description = models.CharField(max_length=250, blank=True, null=True)
    to = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='pending')


    def __str__(self):
        return self.tx_hash