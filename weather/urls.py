from django.urls import path
from .views import get_weather
from . import views

urlpatterns = [
    path("weather/", get_weather, name="get_weather"),
    path("download-report/", views.download_report),
]