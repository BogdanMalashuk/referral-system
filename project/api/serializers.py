from rest_framework import serializers
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()
    activated_code = serializers.CharField(source='activated_code.invite_code', read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_code', 'referrals']

    @staticmethod
    def get_referrals(obj):
        return list(User.objects.filter(activated_code=obj).values_list('phone_number', flat=True))
