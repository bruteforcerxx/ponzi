from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    referrer_id = models.IntegerField(default=0, blank=True, null=True)
    wallet_address = models.CharField(max_length=200, blank=True, null=True, unique=True)
    to_wallet = models.CharField(max_length=200, blank=True, null=True)
    level = models.IntegerField(null=True, blank=True, default=0)
    phone = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

    def get_referrer(self):
        referrer = User.objects.get(id = self.referrer_id)
        return referrer

    def get_downlines(self):
        downlines = User.objects.filter(referrer_id = self.id)
        return downlines