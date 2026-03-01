from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("api/", include("predictions.urls")),
    path("api/", include("weather.urls")), 
    path("api/", include("assistant.urls")),
]
