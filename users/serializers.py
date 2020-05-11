from rest_framework import serializers
from .models import User    

class UserSerializer(serializers.ModelSerializer):
    referrer = serializers.SerializerMethodField()
    downlines = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ['groups', 'is_staff', 'user_permissions']
        # depth = 1
        # fields = ['email', 'username', 'referrer_id']


    def get_referrer(self, obj):
        # try:
        #     user = User.objects.get(id = obj.referrer.id)
        #     referrer = {
        #         'id': user.id,
        #         'username': user.username,
        #         'level': user.level
        #     }
        # except (User.DoesNotExist, AttributeError):
        #     referrer = None
        return obj.get_referrer()

    def get_downlines(self, obj):
        # users = User.objects.filter(referrer = obj)
        # data = []
        # for user in users:
        #     data.append({
        #         'id': user.id,
        #         'username': user.username,
        #         'level': user.level,
        #         'downlines': user.get_downlines()
        #     })
        return obj.get_downlines()
            