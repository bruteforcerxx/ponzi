from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.
CHOICES = [
    ('pending', 'pending'),
    ('complete', 'successful'),
    ('failed', 'failed')
]

class Transaction(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    tx_hash = models.CharField(max_length=400)
    amount = models.IntegerField()
    type = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)
    to = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=200, choices=CHOICES, default='pending')

    def __str__(self):
        return self.tx_hash