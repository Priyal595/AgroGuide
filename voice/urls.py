"""
voice/urls.py
All URL patterns for the Voice Assistant app.
These are included under the "voice/" prefix in core/urls.py.
"""
from django.urls import path
from . import views

app_name = "voice"

urlpatterns = [
    # ── Page (renders the HTML UI) ───────────────────────────────────────
    path("",                views.voice_assistant_page, name="assistant"),

    # ── JSON API endpoints ───────────────────────────────────────────────
    path("process-text/",   views.process_text,         name="process_text"),
    path("process-audio/",  views.process_audio,        name="process_audio"),
    path("weather/",        views.get_weather,           name="weather"),
    path("crop-prices/",    views.get_crop_prices,       name="crop_prices"),
    path("gov-schemes/",    views.get_gov_schemes,       name="gov_schemes"),
    path("reverse-geocode/",views.api_reverse_geocode,   name="reverse_geocode"),
    path("history/",        views.query_history,         name="history"),
]
