from django.shortcuts import render, redirect
from api.models import User, VerificationCode
from api.views import generate_invite_code
import time


def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number")
        if not phone:
            return render(request, "login.html", {"error": "Введите номер телефона"})

        time.sleep(1)
        code = VerificationCode.generate_code()
        VerificationCode.objects.create(phone_number=phone, code=code)
        print(f"Auth code for {phone}: {code}")
        request.session["phone_number"] = phone
        return redirect("verify")
    return render(request, "login.html")


def verify_view(request):
    phone = request.session.get("phone_number")
    if not phone:
        return redirect("login")

    if request.method == "POST":
        code = request.POST.get("code")
        verif = (
            VerificationCode.objects.filter(phone_number=phone)
            .order_by("-created_at")
            .first()
        )
        if not verif or verif.code != code or verif.is_expired():
            return render(request, "verify.html", {"error": "Неверный или просроченный код"})

        user, created = User.objects.get_or_create(phone_number=phone)

        if created:
            while True:
                invite_code = generate_invite_code()
                if not User.objects.filter(invite_code=invite_code).exists():
                    user.invite_code = invite_code
                    user.save()
                    break

        request.session["user_id"] = user.id
        return redirect("profile")

    return render(request, "verify.html")


def profile_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")

    referrals = list(User.objects.filter(activated_code=user).values_list("phone_number", flat=True))
    referral_count = len(referrals)

    context = {
        "profile": {
            "phone_number": user.phone_number,
            "invite_code": user.invite_code,
            "activated_code": user.activated_code.invite_code if user.activated_code else None,
            "referrals": referrals,
            "referral_count": referral_count,
        }
    }
    return render(request, "profile.html", context)


def activate_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")

    if user.activated_code:
        context = {
            "activated_code": user.activated_code.invite_code,
        }
        return render(request, "activate.html", context)

    if request.method == "POST":
        code = request.POST.get("code")
        inviter = User.objects.filter(invite_code=code).first()
        if not inviter:
            return render(request, "activate.html", {"error": "Неверный инвайт-код"})
        if inviter == user:
            return render(request, "activate.html", {"error": "Нельзя использовать свой инвайт-код"})
        user.activated_code = inviter
        user.save()
        return redirect("profile")

    return render(request, "activate.html")
