"""
voice/views.py
--------------
All Django views for the Voice Assistant feature.
Every API endpoint returns JSON so the frontend JavaScript can consume it.
"""

import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render

from .models import VoiceQuery
from .services import (
    generate_ai_response,
    generate_schemes_response,
    synthesize_speech,
    recognize_speech_with_azure,
    fetch_weather,
    fetch_crop_price,
    reverse_geocode,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _json_body(request) -> dict:
    """Safely parse the JSON body of a request."""
    try:
        return json.loads(request.body)
    except Exception:
        return {}


def _user_location(user) -> str:
    """
    Try to get the user's saved location from their profile.
    Falls back to 'India' if no profile / location is set.
    Adjust the attribute name to match YOUR profile model.
    """
    try:
        # Common attribute names — change 'location' to whatever yours is
        loc = getattr(user, 'profile', None)
        if loc:
            return getattr(loc, 'location', 'India') or 'India'
    except Exception:
        pass
    return 'India'


# ---------------------------------------------------------------------------
# Page view  –  renders the HTML template
# ---------------------------------------------------------------------------

@login_required
def voice_assistant_page(request):
    """GET /voice/  →  renders the voice assistant UI."""
    recent = VoiceQuery.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'voice/voice_assistant.html', {'recent_queries': recent})


# ---------------------------------------------------------------------------
# API: Process text
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def process_text(request):
    """
    POST /voice/process-text/
    Body (JSON): { "text": "...", "language": "en" }
    Response:    { "response_text": "...", "audio_data": "<base64 or null>" }
    """
    data     = _json_body(request)
    text     = data.get('text', '').strip()
    language = data.get('language', 'en')

    if not text:
        return JsonResponse({'error': 'No text provided.'}, status=400)

    try:
        location      = _user_location(request.user)
        response_text = generate_ai_response(text, location, language)

        VoiceQuery.objects.create(
            user=request.user,
            query=text,
            response=response_text,
            query_type='text',
            language=language,
        )

        audio_data = synthesize_speech(response_text, language)
        return JsonResponse({'response_text': response_text, 'audio_data': audio_data})

    except Exception as exc:
        logger.exception('process_text error')
        return JsonResponse({'error': str(exc)}, status=500)


# ---------------------------------------------------------------------------
# API: Process audio
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def process_audio(request):
    """
    POST /voice/process-audio/
    Form data: file=<audio blob>, language=<code>
    Response:  { "transcript": "...", "response_text": "...", "audio_data": "..." }
    """
    audio_file = request.FILES.get('file')
    language   = request.POST.get('language', 'en')

    if not audio_file:
        return JsonResponse({'error': 'No audio file uploaded.'}, status=400)

    try:
        audio_bytes = audio_file.read()
        logger.info(f'[voice] audio received: {len(audio_bytes)} bytes, lang={language}')

        transcript    = recognize_speech_with_azure(audio_bytes, language)
        location      = _user_location(request.user)
        response_text = generate_ai_response(transcript, location, language)

        VoiceQuery.objects.create(
            user=request.user,
            query=transcript,
            response=response_text,
            query_type='audio',
            language=language,
        )

        audio_data = synthesize_speech(response_text, language)
        return JsonResponse({
            'transcript':    transcript,
            'response_text': response_text,
            'audio_data':    audio_data,
        })

    except ValueError as exc:
        # speech not recognised
        return JsonResponse({'error': str(exc)}, status=400)
    except Exception as exc:
        logger.exception('process_audio error')
        return JsonResponse({'error': str(exc)}, status=500)


# ---------------------------------------------------------------------------
# API: Weather
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def get_weather(request):
    """
    POST /voice/weather/
    Body: { "city": "Mumbai", "language": "en" }
    """
    data     = _json_body(request)
    city     = data.get('city', '').strip()
    language = data.get('language', 'en')

    if not city or city.lower() == 'current':
        city = _user_location(request.user).split(',')[0].strip()

    try:
        weather    = fetch_weather(city)
        audio_data = synthesize_speech(weather['text'], language)
        return JsonResponse({'text': weather['text'], 'audio_data': audio_data})
    except Exception as exc:
        logger.exception('weather error')
        return JsonResponse({'error': str(exc)}, status=500)


# ---------------------------------------------------------------------------
# API: Crop prices
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def get_crop_prices(request):
    """
    POST /voice/crop-prices/
    Body: { "crop": "wheat", "market": "Delhi", "language": "en" }
    """
    data     = _json_body(request)
    crop     = data.get('crop', '').strip()
    language = data.get('language', 'en')
    market   = data.get('market', '').strip() or _user_location(request.user).split(',')[0].strip()

    if not crop:
        return JsonResponse({'error': 'No crop name provided.'}, status=400)

    try:
        text       = fetch_crop_price(crop, market)
        audio_data = synthesize_speech(text, language)
        return JsonResponse({'text': text, 'audio_data': audio_data})
    except Exception as exc:
        logger.exception('crop prices error')
        return JsonResponse({'error': str(exc)}, status=500)


# ---------------------------------------------------------------------------
# API: Government schemes
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def get_gov_schemes(request):
    """
    POST /voice/gov-schemes/
    Body: { "topic": "irrigation", "language": "en" }
    """
    data     = _json_body(request)
    topic    = data.get('topic', '').strip()
    language = data.get('language', 'en')

    if not topic:
        return JsonResponse({'error': 'No topic provided.'}, status=400)

    try:
        text       = generate_schemes_response(topic)
        audio_data = synthesize_speech(text, language)
        return JsonResponse({'text': text, 'audio_data': audio_data})
    except Exception as exc:
        logger.exception('gov schemes error')
        return JsonResponse({'error': str(exc)}, status=500)


# ---------------------------------------------------------------------------
# API: Reverse geocode
# ---------------------------------------------------------------------------

@csrf_exempt
@login_required
@require_POST
def api_reverse_geocode(request):
    """
    POST /voice/reverse-geocode/
    Body: { "latitude": 28.6, "longitude": 77.2 }
    """
    data = _json_body(request)
    try:
        lat = float(data['latitude'])
        lon = float(data['longitude'])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({'error': 'Invalid or missing latitude/longitude.'}, status=400)

    address = reverse_geocode(lat, lon)
    return JsonResponse({'address': address, 'coordinates': {'latitude': lat, 'longitude': lon}})


# ---------------------------------------------------------------------------
# API: Query history
# ---------------------------------------------------------------------------

@login_required
@require_GET
def query_history(request):
    """
    GET /voice/history/
    Returns last 20 queries for the logged-in user as JSON.
    """
    queries = VoiceQuery.objects.filter(user=request.user).order_by('-timestamp')[:20]
    return JsonResponse({
        'history': [
            {
                'id':         q.id,
                'query':      q.query,
                'response':   q.response,
                'query_type': q.query_type,
                'language':   q.language,
                'timestamp':  q.timestamp.isoformat(),
            }
            for q in queries
        ]
    })
