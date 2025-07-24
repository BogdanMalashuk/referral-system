from rest_framework import serializers


class RequestCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()


class ActivateInviteCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
