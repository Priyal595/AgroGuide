"""
voice/services.py
-----------------
STT  : Azure Whisper  (primary)  →  Azure Speech REST  (fallback)
TTS  : Azure Speech SDK
AI   : Azure OpenAI  (language-enforced)
Other: OpenWeatherMap + crop alerts, crop prices, gov schemes, reverse geocode
"""

import os
import io
import base64
import tempfile
import requests
from typing import Optional
from django.conf import settings


# ─────────────────────────────────────────────────────────────────────────────
# Language maps
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_TO_LOCALE = {
    "en": "en-US",
    "hi": "hi-IN",
    "mr": "mr-IN",
    "bn": "bn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
}

LANGUAGE_TO_NAME = {
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
}

# ISO-639-1 codes for Whisper
LANGUAGE_TO_WHISPER = {
    "en": "en",
    "hi": "hi",
    "mr": "mr",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
}


# ─────────────────────────────────────────────────────────────────────────────
# Lazy Azure OpenAI client
# ─────────────────────────────────────────────────────────────────────────────
_azure_client = None

def _get_azure_client():
    global _azure_client
    if _azure_client is None:
        from openai import AzureOpenAI
        _azure_client = AzureOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )
    return _azure_client


# ─────────────────────────────────────────────────────────────────────────────
# Helper: language instruction injected into every system prompt
# ─────────────────────────────────────────────────────────────────────────────
def _lang_instr(language: str) -> str:
    name = LANGUAGE_TO_NAME.get(language, "English")
    return (
        f"IMPORTANT: You MUST reply ONLY in {name}. "
        f"Do NOT use any other language. "
        f"Even if the user writes in another language, always respond in {name}."
    )


# ─────────────────────────────────────────────────────────────────────────────
# 1.  SPEECH-TO-TEXT
#     Primary  : Azure Whisper  (your AZURE_WHISPER_KEY + AZURE_WHISPER_ENDPOINT)
#     Fallback : Azure Speech REST  (your AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)
# ─────────────────────────────────────────────────────────────────────────────
def recognize_speech_with_azure(audio_bytes: bytes, language: str) -> str:
    """
    Try Azure Whisper first.
    If it fails or credentials are missing, fall back to Azure Speech STT.
    Raises ValueError if both fail (user-visible message).
    """

    # ── Try Azure Whisper ─────────────────────────────────────────────────
    whisper_key      = getattr(settings, "AZURE_WHISPER_KEY",      "").strip()
    whisper_endpoint = getattr(settings, "AZURE_WHISPER_ENDPOINT",  "").strip()
    whisper_version  = getattr(settings, "AZURE_API_VERSION",       "2024-12-01-preview").strip()

    if whisper_key and whisper_endpoint:
        try:
            print(f"[voice STT] Trying Azure Whisper for lang={language}…")
            transcript = _azure_whisper_stt(audio_bytes, language,
                                            whisper_key, whisper_endpoint,
                                            whisper_version)
            if transcript:
                print(f"[voice STT] Azure Whisper OK: '{transcript[:60]}…'")
                return transcript
            print("[voice STT] Azure Whisper returned empty, trying fallback…")
        except Exception as e:
            print(f"[voice STT] Azure Whisper failed ({e}), trying Speech REST fallback…")

    # ── Fallback: Azure Speech REST ───────────────────────────────────────
    speech_key    = getattr(settings, "AZURE_SPEECH_KEY",    "").strip()
    speech_region = getattr(settings, "AZURE_SPEECH_REGION", "").strip()

    if speech_key and speech_region:
        try:
            print(f"[voice STT] Trying Azure Speech REST for lang={language}…")
            transcript = _azure_speech_rest_stt(audio_bytes, language,
                                                speech_key, speech_region)
            if transcript:
                print(f"[voice STT] Azure Speech REST OK: '{transcript[:60]}…'")
                return transcript
            print("[voice STT] Azure Speech REST returned empty transcript.")
        except Exception as e:
            print(f"[voice STT] Azure Speech REST also failed: {e}")

    raise ValueError(
        "Could not recognise speech. Please check your Azure credentials in .env, "
        "or try speaking more clearly and closer to the microphone."
    )


def _azure_whisper_stt(audio_bytes: bytes, language: str,
                       api_key: str, endpoint: str, api_version: str) -> str:
    """
    Transcribe using Azure-hosted Whisper via the Azure AI Services REST API.
    Endpoint format:  https://YOUR-RESOURCE.services.ai.azure.com/
    Full URL becomes: {endpoint}openai/deployments/whisper/audio/transcriptions?api-version=...
    """
    # Normalise endpoint — strip trailing slash then build full URL
    base  = endpoint.rstrip("/")
    url   = f"{base}/openai/deployments/whisper/audio/transcriptions?api-version={api_version}"

    whisper_lang = LANGUAGE_TO_WHISPER.get(language, "en")

    # Write bytes to a temp file so requests can send it as multipart
    suffix = ".webm"  # browser records webm; Whisper accepts it fine
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            files   = {"file": (f"audio{suffix}", f, "audio/webm")}
            data    = {"language": whisper_lang}
            headers = {"api-key": api_key}

            resp = requests.post(url, headers=headers, files=files, data=data, timeout=60)

        if resp.status_code != 200:
            raise RuntimeError(
                f"Azure Whisper {resp.status_code}: {resp.text[:300]}"
            )

        result = resp.json()
        return (result.get("text") or "").strip()

    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _azure_speech_rest_stt(audio_bytes: bytes, language: str,
                            speech_key: str, speech_region: str) -> str:
    """
    Transcribe using Azure Cognitive Services Speech-to-Text REST endpoint.
    Expects WAV/PCM audio; works with webm too (Azure is lenient).
    """
    locale = LANGUAGE_TO_LOCALE.get(language, "en-US")
    url    = (
        f"https://{speech_region}.stt.speech.microsoft.com"
        f"/speech/recognition/conversation/cognitiveservices/v1"
    )
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type":              "audio/wav; codecs=audio/pcm; samplerate=16000",
    }
    resp = requests.post(
        url, headers=headers,
        params={"language": locale},
        data=audio_bytes, timeout=30
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Azure Speech REST {resp.status_code}: {resp.text[:300]}")

    try:
        data = resp.json()
    except ValueError:
        raise RuntimeError("Azure Speech REST returned invalid JSON.")

    return (data.get("DisplayText") or data.get("Text") or "").strip()


# ─────────────────────────────────────────────────────────────────────────────
# 2.  TEXT-TO-SPEECH  (Azure Speech SDK)
# ─────────────────────────────────────────────────────────────────────────────
def synthesize_speech(text: str, language: str) -> Optional[str]:
    """
    Convert text → speech using Azure Cognitive Services TTS.
    Returns base64-encoded WAV string, or None (frontend uses browser TTS).
    """
    speech_key    = getattr(settings, "AZURE_SPEECH_KEY",    "").strip()
    speech_region = getattr(settings, "AZURE_SPEECH_REGION", "").strip()

    if not speech_key or not speech_region or not text:
        print("[voice TTS] No Azure Speech credentials — skipping TTS (browser fallback will be used).")
        return None

    try:
        import azure.cognitiveservices.speech as speechsdk

        locale        = LANGUAGE_TO_LOCALE.get(language, "en-US")
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_language = locale

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None
        )
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return base64.b64encode(result.audio_data).decode("utf-8")

        if result.reason == speechsdk.ResultReason.Canceled:
            details = speechsdk.CancellationDetails.from_result(result)
            print(f"[voice TTS] Cancelled: {details.reason} – {details.error_details}")

    except ImportError:
        print("[voice TTS] azure-cognitiveservices-speech not installed. Run: pip install azure-cognitiveservices-speech")
    except Exception as e:
        print(f"[voice TTS] Error: {e}")

    return None


# ─────────────────────────────────────────────────────────────────────────────
# 3.  AI CHAT RESPONSE  (Azure OpenAI, language-enforced)
# ─────────────────────────────────────────────────────────────────────────────
def generate_ai_response(user_text: str, user_location: str, language: str) -> str:
    client     = _get_azure_client()
    deployment = getattr(settings, "AZURE_OPENAI_DEPLOYMENT", "gpt35")

    result = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Gram Vaani, an AI Voice Assistant for farmers in rural India. "
                    "Help with farming advice, weather, crop prices and government schemes. "
                    f"The user is in {user_location}. "
                    f"{_lang_instr(language)}"
                ),
            },
            {"role": "user", "content": user_text},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return result.choices[0].message.content


# ─────────────────────────────────────────────────────────────────────────────
# 4.  GOVERNMENT SCHEMES  (language-enforced)
# ─────────────────────────────────────────────────────────────────────────────
def generate_schemes_response(topic: str, language: str = "en") -> str:
    client     = _get_azure_client()
    deployment = getattr(settings, "AZURE_OPENAI_DEPLOYMENT", "gpt35")

    result = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Gram Vaani, an AI assistant for rural India. "
                    "Explain Indian government schemes for farmers clearly and simply. "
                    f"{_lang_instr(language)}"
                ),
            },
            {
                "role": "user",
                "content": f"Tell me about government schemes related to: {topic}",
            },
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return result.choices[0].message.content


# ─────────────────────────────────────────────────────────────────────────────
# 5.  WEATHER  +  CROP ALERTS
# ─────────────────────────────────────────────────────────────────────────────
ALERT_RULES = [
    (lambda d: d["temp"] > 40,
     "🔴 HEAT ALERT: Temperature above 40°C. Risk of heat stress on wheat, rice and vegetables. "
     "Irrigate in early morning or evening only. Avoid transplanting seedlings."),

    (lambda d: d["temp"] < 5,
     "🔵 FROST ALERT: Temperature below 5°C. Risk of frost damage. "
     "Cover young plants, delay sowing of warm-season crops."),

    (lambda d: d["humidity"] > 85,
     "🟡 HIGH HUMIDITY ALERT: Humidity above 85%. High risk of fungal diseases "
     "(blight, mildew, rust). Apply preventive fungicide. Ensure good field drainage."),

    (lambda d: d["humidity"] < 30,
     "🟠 DRY CONDITIONS ALERT: Humidity below 30%. Increased water stress risk. "
     "Monitor soil moisture closely and increase irrigation frequency."),

    (lambda d: d["wind_speed"] > 15,
     "💨 STRONG WIND ALERT: Wind above 15 m/s. Risk of lodging in tall crops "
     "(sugarcane, maize, sorghum). Avoid spraying pesticides/fertilizers today."),

    (lambda d: d["weather_id"] in range(200, 300),
     "⛈️ THUNDERSTORM ALERT: Thunderstorms expected. Stay off open fields. "
     "Secure farm equipment. Risk of hail damage to standing crops."),

    (lambda d: d["weather_id"] in range(500, 510),
     "🌧️ HEAVY RAIN ALERT: Heavy rainfall expected. Risk of waterlogging and root rot. "
     "Clear drainage channels. Delay pesticide and fertilizer application."),

    (lambda d: d["weather_id"] in range(600, 700),
     "❄️ SNOW/SLEET ALERT: Snow or sleet possible. Protect crops with covers. "
     "Delay all field operations until conditions improve."),

    (lambda d: d["weather_id"] in range(700, 800),
     "🌫️ FOG/HAZE ALERT: Reduced visibility and high moisture. "
     "Watch for disease outbreaks. Inspect crops for early blight or rust symptoms."),
]


def _generate_crop_alerts(weather_data: dict) -> list:
    alerts = []
    for condition_fn, message in ALERT_RULES:
        try:
            if condition_fn(weather_data):
                alerts.append(message)
        except Exception:
            pass
    return alerts


def fetch_weather(city: str, language: str = "en") -> dict:
    api_key = getattr(settings, "OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is missing from your .env file. "
            "Get a free key at openweathermap.org."
        )

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    res = requests.get(url, timeout=10)

    if res.status_code == 401:
        raise RuntimeError("Invalid OPENWEATHER_API_KEY. Please check openweathermap.org.")
    if res.status_code == 404:
        raise RuntimeError(f"City '{city}' not found. Check the spelling.")
    if res.status_code != 200:
        raise RuntimeError(f"Weather API error {res.status_code}: {res.text}")

    d            = res.json()
    weather_id   = d["weather"][0]["id"]
    weather_desc = d["weather"][0]["description"]
    weather_icon = d["weather"][0]["icon"]
    temp         = d["main"]["temp"]
    feels_like   = d["main"]["feels_like"]
    humidity     = d["main"]["humidity"]
    wind_speed   = d.get("wind", {}).get("speed", 0)
    visibility   = d.get("visibility", 10000) // 1000

    summary = (
        f"Weather in {city}: {weather_desc.capitalize()}, "
        f"temperature {temp}°C (feels like {feels_like}°C), "
        f"humidity {humidity}%, wind {wind_speed} m/s, "
        f"visibility {visibility} km."
    )

    raw_data = {
        "temp": temp, "humidity": humidity,
        "wind_speed": wind_speed, "weather_id": weather_id,
    }
    alerts = _generate_crop_alerts(raw_data)

    # Translate alerts to chosen language
    if language != "en" and alerts:
        try:
            client     = _get_azure_client()
            deployment = getattr(settings, "AZURE_OPENAI_DEPLOYMENT", "gpt35")
            trans = client.chat.completions.create(
                model=deployment,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Translate each crop weather alert below into the requested language. "
                            "Keep each alert on its own line. Keep the emoji at the start. "
                            f"{_lang_instr(language)}"
                        ),
                    },
                    {"role": "user", "content": "\n".join(alerts)},
                ],
                max_tokens=800, temperature=0,
            )
            translated = trans.choices[0].message.content.strip().split("\n")
            alerts = [a for a in translated if a.strip()]
        except Exception as e:
            print(f"[voice] Alert translation failed: {e}")

    return {
        "text":       summary,
        "alerts":     alerts,
        "alert_text": "\n".join(alerts),
        "city":       city,
        "temp":       temp,
        "feels_like": feels_like,
        "humidity":   humidity,
        "wind_speed": wind_speed,
        "desc":       weather_desc,
        "icon":       weather_icon,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6.  CROP PRICES  (static MSP table — replace with real API if needed)
# ─────────────────────────────────────────────────────────────────────────────
_CROP_PRICES = {
    "wheat": 2275, "rice": 2183, "corn": 1760, "barley": 1735,
    "sugarcane": 3150, "cotton": 6620, "soybean": 4600, "mustard": 5650,
    "onion": 3000, "potato": 1400, "tomato": 3600, "chili": 8000,
    "maize": 1760, "groundnut": 6377, "sunflower": 6760, "jowar": 3180,
    "bajra": 2500, "tur": 7000, "moong": 8558, "urad": 6950,
}


def fetch_crop_price(crop: str, market: str, language: str = "en") -> str:
    price   = _CROP_PRICES.get(crop.lower(), 2500)
    text_en = (
        f"Current MSP (Minimum Support Price) for {crop} is ₹{price} per quintal "
        f"(as per government rates). Market price in {market} may vary."
    )
    if language == "en":
        return text_en

    try:
        client     = _get_azure_client()
        deployment = getattr(settings, "AZURE_OPENAI_DEPLOYMENT", "gpt35")
        result = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": f"Translate this crop price information accurately. {_lang_instr(language)}",
                },
                {"role": "user", "content": text_en},
            ],
            max_tokens=150, temperature=0,
        )
        return result.choices[0].message.content.strip()
    except Exception:
        return text_en


# ─────────────────────────────────────────────────────────────────────────────
# 7.  REVERSE GEOCODE  (Nominatim — no API key needed)
# ─────────────────────────────────────────────────────────────────────────────
def reverse_geocode(latitude: float, longitude: float) -> str:
    url = (
        f"https://nominatim.openstreetmap.org/reverse"
        f"?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    )
    headers = {"User-Agent": "AgroGuide-VoiceApp/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            addr  = resp.json().get("address", {})
            parts = []
            for key in ("village", "town", "city"):
                if addr.get(key):
                    parts.append(addr[key])
                    break
            for key in ("state_district", "state", "postcode"):
                val = addr.get(key, "")
                if val and val not in parts:
                    parts.append(val)
            return ", ".join(filter(None, parts)) or f"{latitude:.4f}, {longitude:.4f}"
    except Exception as e:
        print(f"[voice geocode] {e}")
    return f"{latitude:.4f}, {longitude:.4f}"