from django.db import models
from django.contrib.auth.models import AbstractUser
from ponzi.settings import AUTH_USER_MODEL
from rest_framework import serializers
import random
import string

def get_referral_code(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)referral_code = models.CharField(max_length=100, default=get_referral_code(), unique=True) #code for referring others
    referrer_code = models.CharField(max_length=100, null=True, blank=True) #code of the person who referred the user
    wallet_address = models.CharField(max_length=200, blank=True, null=True, unique=True)
    to_wallet = models.CharField(max_length=200, blank=True, null=True, unique=True)
    balance = models.DecimalField(max_digits=50, decimal_places=8, default=0.00000000)
    level = models.IntegerField(null=True, blank=True, default=0)
    phone = models.PositiveIntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_referrer(self):
        try:
            user = User.objects.get(referral_code = self.referrer_code)
            upline = {
                'id': user.id,
                'username': user.username,
                'level': user.level,
                'referral_code': user.referral_code
            }
        except:
            upline = 'null'
        return upline

    def get_downlines(self):
        downlines = User.objects.filter(referrer_code = self.referral_code)
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