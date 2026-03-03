from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("api/", include("predictions.urls")),
    path("api/", include("weather.urls")), 
<<<<<<< HEAD
    path('learn/', include('learning.urls')),
=======
    path("api/", include("assistant.urls")),
    path("api/chatbot/", include("guided_chatbot.urls")),
>>>>>>> 115ee52 (added rule-based guided chatbot)
]
