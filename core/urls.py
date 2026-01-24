"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.shortcuts import render


# ---------- Frontend-only Views ----------
def landing(request):
    return render(request, "landing.html")

def login_view(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def dashboard(request):
    return render(request, "dashboard.html")

def email_verification(request):
    return render(request, "verify_status.html", {"success": True})

def resend_verification(request):
    return render(request, "verify_status.html", {"success": False})


def logout_view(request):
    return render(request, "landing.html")


# ---------- URL Patterns ----------
urlpatterns = [
    path("admin/", admin.site.urls),

    # Public pages
    path("", landing, name="landing"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),

    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),

    # Email verification
    path("verify-email/", email_verification, name="verify_email"),
    path("resend-verification/", resend_verification, name="resend_verification"),

    # Logout (temporary frontend-only)
    path("logout/", logout_view, name="logout"),
]
