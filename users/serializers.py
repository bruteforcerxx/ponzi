from rest_framework import serializers
from .models import User 
from ponzi.settings import AUTH_USER_MODEL   
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

class UserSerializer(serializers.ModelSerializer):
    upline = serializers.SerializerMethodField()
    downlines = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ['groups', 'is_staff', 'user_permissions', 'password']
        # depth = 1
        # fields = ['email', 'username', 'referrer_id']


    def get_upline(self, obj):
        return obj.get_referrer()

    def get_downlines(self, obj):
        return obj.get_downlines()
            


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ( 'password', )