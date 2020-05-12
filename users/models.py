from django.db import models
from django.contrib.auth.models import AbstractUser
from ponzi.settings import AUTH_USER_MODEL
from rest_framework import serializers

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    referrer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # referrer_id = models.IntegerField(default=0, blank=True,   null=True)
    wallet_address = models.CharField(max_length=200, blank=True, null=True, unique=True)
    to_wallet = models.CharField(max_length=200, blank=True, null=True, unique=True)
    balance = models.DecimalField(max_digits=50, decimal_places=8, default=0.00000000)
    level = models.IntegerField(null=True, blank=True, default=0)
    phone = models.PositiveIntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'referrer', 'level', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_referrer(self):
        try:
            user = User.objects.get(id = self.referrer.id)
            referrer = {
                'id': user.id,
                'username': user.username,
                'level': user.level
            }
        except:
            referrer = 'null'
        return referrer

    def get_downlines(self):
        downlines = User.objects.filter(referrer = self)
        data = []
        for user in downlines:
            data.append({
                'id': user.id,
                'username': user.username,
                'level': user.level,
                # 'downlines': user.get_downlines(),
                # 'referrer': user.get_referrer()
            })
        return data