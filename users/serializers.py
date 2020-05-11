from rest_framework import serializers
from .models import User
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    referrer = serializers.SerializerMethodField()
    downlines = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ['password', 'groups', 'is_staff', 'user_permissions']
        # fields = ['email', 'username', 'referrer_id']


    def get_referrer(self, obj):
        try:
            user = User.objects.get(id = obj.referrer_id)
            uplink = {
                'id': user.id,
                'username': user.username,
                'referrer_id': user.referrer_id
            }
        except User.DoesNotExist:
            uplink = None
        return uplink

    def get_downlines(self, obj):
        users = User.objects.filter(referrer_id = obj.id)
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'username': user.username,
            })
        return data
            