from django.urls import path
from .views import assistant_api

urlpatterns = [
    path("assistant/", assistant_api, name="assistant_api"),
]