from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'is_staff', 'user_permissions']
        # fields = ['email', 'username', 'referrer_id']