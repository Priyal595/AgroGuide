from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def landing(request):
    return render(request, "landing.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "login.html", {
                    "error": "Please verify your email before logging in."
                })
        else:
            return render(request, "login.html", {
                "error": "Invalid email or password."
            })

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1. Passwords must match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # 2. Email must be unique
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect("register")

        # 3. Auto-generate username
        username = email.split("@")[0]
        if User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count()}"

        # 4. Create inactive user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.is_active = False
        user.save()

        # 5. Generate verification token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_link = request.build_absolute_uri(
            f"/verify-email/{uid}/{token}/"
        )

        # 6. Send verification email (console backend)
        send_mail(
            subject="Verify your CropAdvisor account",
            message=f"Click the link below to verify your account:\n\n{verify_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return render(request, "verify_status.html", {"success": False})

    return render(request, "register.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "verify_status.html", {"success": True})
    return render(request, "verify_status.html", {"success": False})


def logout_view(request):
    logout(request)
    return redirect("landing")

def resend_verification(request):
    # For now, just show "check your email" again
    return render(request, "verify_status.html", {"success": False})
