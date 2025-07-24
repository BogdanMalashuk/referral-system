import time
import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import User, VerificationCode
from .serializers import ProfileSerializer
from .doc_serializers import (
    RequestCodeSerializer,
    VerifyCodeSerializer,
    ActivateInviteCodeSerializer
)


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@extend_schema(
    request=RequestCodeSerializer,
    responses={200: serializers.DictField()},
    examples=[
        OpenApiExample(
            name="Request SMS Code",
            value={"phone_number": "+375441234567"},
        )
    ],
)
class RequestCodeView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        phone = request.data.get('phone_number')
        if not phone:
            return Response({"error": "Phone number required"}, status=400)

        time.sleep(1)
        code = VerificationCode.generate_code()
        VerificationCode.objects.create(phone_number=phone, code=code)
        print(f"Auth code for {phone}: {code}")
        return Response({"message": "Code sent (simulated)"})


@extend_schema(
    request=VerifyCodeSerializer,
    responses={200: serializers.DictField()},
)
class VerifyCodeView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('code')

        verif = VerificationCode.objects.filter(phone_number=phone).order_by('-created_at').first()
        if not verif or verif.code != code or verif.is_expired():
            return Response({"error": "Invalid or expired code"}, status=400)

        user, created = User.objects.get_or_create(phone_number=phone)
        if created:
            while True:
                invite_code = generate_invite_code()
                if not User.objects.filter(invite_code=invite_code).exists():
                    user.invite_code = invite_code
                    user.save()
                    break

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


@extend_schema(
    responses=ProfileSerializer,
)
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


@extend_schema(
    request=ActivateInviteCodeSerializer,
    responses={200: serializers.DictField()},
)
class ActivateInviteCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        code = request.data.get('code')
        if request.user.activated_code:
            return Response({"error": "Invite code already activated"}, status=400)

        inviter = User.objects.filter(invite_code=code).first()
        if not inviter:
            return Response({"error": "Invalid invite code"}, status=404)

        if inviter == request.user:
            return Response({"error": "Cannot use your own invite code"}, status=400)

        request.user.activated_code = inviter
        request.user.save()
        return Response({"message": "Invite code activated"})
