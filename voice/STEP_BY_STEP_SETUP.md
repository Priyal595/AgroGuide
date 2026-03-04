# ✅ Voice Assistant – Complete Step-by-Step Setup Guide

---

## 🔑 WHAT API KEYS DO YOU NEED?

You need keys from TWO services:

### 1. Azure OpenAI  (for the AI brain / chat responses)
Go to: https://portal.azure.com
- Create an "Azure OpenAI" resource
- Deploy a model (e.g. gpt-35-turbo) and give it a deployment name (e.g. "gpt35")
- Keys you get:
  - AZURE_OPENAI_ENDPOINT   → looks like: https://your-name.openai.azure.com/
  - AZURE_OPENAI_API_KEY    → a long string of letters/numbers
  - AZURE_OPENAI_DEPLOYMENT → the name you gave your deployed model (e.g. "gpt35")
  - AZURE_OPENAI_API_VERSION → use: 2024-12-01-preview

### 2. Azure Speech (for voice recording → text, and text → voice playback)
Go to: https://portal.azure.com
- Create a "Speech" resource (also called Cognitive Services Speech)
- Keys you get:
  - AZURE_SPEECH_KEY    → a long string
  - AZURE_SPEECH_REGION → e.g. "eastus" or "centralindia"

### 3. OpenWeatherMap  (for weather queries)
Go to: https://openweathermap.org/api
- Create a free account, get an API key
  - OPENWEATHER_API_KEY → a short string

### ⚠️ NOTE: Speech keys are OPTIONAL
If you don't have Azure Speech keys yet, the app still works perfectly:
- Text responses will show on screen
- Browser's built-in text-to-speech will be used as a fallback
- Voice recording will show an error until you add the keys

---

## 📁 WHERE TO PUT EVERY FILE

Your project is at: D:\backup\WE\CAPSTONE\voicebot\AgroGuide\

Here is the EXACT target location for every file:

```
AgroGuide/                              ← your project root (where manage.py is)
│
├── voice/                              ← CREATE this folder
│   ├── __init__.py                     ← empty file (required)
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── admin.py
│   └── migrations/
│       ├── __init__.py                 ← empty file (required)
│       └── 0001_initial.py
│
└── templates/
    └── voice/                          ← CREATE this sub-folder inside existing templates/
        └── voice_assistant.html
```

---

## 📝 STEP 1 – Edit your .env file

Open:  AgroGuide/.env

ADD these lines at the bottom (fill in YOUR values):

```
# ── Azure OpenAI ──────────────────────────────────────────────
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE-NAME.openai.azure.com/
AZURE_OPENAI_API_KEY=PASTE_YOUR_AZURE_OPENAI_KEY_HERE
AZURE_OPENAI_DEPLOYMENT=gpt35
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# ── Azure Speech (for voice recording + playback) ─────────────
AZURE_SPEECH_KEY=PASTE_YOUR_SPEECH_KEY_HERE
AZURE_SPEECH_REGION=eastus

# ── OpenWeatherMap ─────────────────────────────────────────────
OPENWEATHER_API_KEY=PASTE_YOUR_WEATHER_KEY_HERE
```

---

## 📝 STEP 2 – Edit core/settings.py

Open:  AgroGuide/core/settings.py

### 2a. Add 'voice' to INSTALLED_APPS

Find the INSTALLED_APPS list and add 'voice' at the end:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... all existing apps ...
    'accounts',
    'predictions',
    'guided_chatbot',
    'learning',
    'weather',
    'voice',              # ← ADD THIS LINE
]
```

### 2b. Add Azure settings at the very bottom of settings.py

```python
import os

# ── Voice Assistant settings ───────────────────────────────────
AZURE_OPENAI_ENDPOINT    = os.environ.get('AZURE_OPENAI_ENDPOINT',    '')
AZURE_OPENAI_API_KEY     = os.environ.get('AZURE_OPENAI_API_KEY',     '')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
AZURE_OPENAI_DEPLOYMENT  = os.environ.get('AZURE_OPENAI_DEPLOYMENT',  'gpt35')
AZURE_SPEECH_KEY         = os.environ.get('AZURE_SPEECH_KEY',         '')
AZURE_SPEECH_REGION      = os.environ.get('AZURE_SPEECH_REGION',      '')
OPENWEATHER_API_KEY      = os.environ.get('OPENWEATHER_API_KEY',      '')
```

---

## 📝 STEP 3 – Edit core/urls.py

Open:  AgroGuide/core/urls.py

It currently looks like this:
```python
urlpatterns = [
    path("admin/",       admin.site.urls),
    path("",             include("accounts.urls")),
    path("api/",         include("predictions.urls")),
    path("api/",         include("weather.urls")),
    path('learn/',       include('learning.urls')),
    path("api/chatbot/", include("guided_chatbot.urls")),
    # path("voice/", ...   ← this is what's failing
]
```

Change it to:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/",       admin.site.urls),
    path("",             include("accounts.urls")),
    path("api/",         include("predictions.urls")),
    path("api/",         include("weather.urls")),
    path('learn/',       include('learning.urls')),
    path("api/chatbot/", include("guided_chatbot.urls")),
    path("voice/",       include("voice.urls", namespace="voice")),   # ← KEEP this line
]
```

The url line is already there — it was failing only because the voice/ folder files were missing.
Now that all files are in place, it will work.

---

## 📝 STEP 4 – Install Python packages

Open your terminal (with venv activated) and run:

```bash
pip install openai requests
```

If you have Azure Speech keys and want voice recording to work, also run:
```bash
pip install azure-cognitiveservices-speech
```

---

## 📝 STEP 5 – Run migrations

In your terminal:
```bash
python manage.py migrate
```

You should see something like:
```
Applying voice.0001_initial... OK
```

---

## 📝 STEP 6 – Add to your navbar

Open your base template (usually templates/base.html or templates/includes/navbar.html)

Find your navbar links and add:

```html
<a href="{% url 'voice:assistant' %}">🎙️ Voice Assistant</a>
```

---

## ✅ STEP 7 – Test it

```bash
python manage.py runserver
```

Go to:  http://127.0.0.1:8000/voice/

You should see the Voice Assistant page!

---

## ❓ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'voice'` | Make sure voice/__init__.py exists |
| `No module named 'openai'` | Run: pip install openai |
| `ImproperlyConfigured: app_name... namespace` | Make sure urls.py has app_name = "voice" |
| Azure speech error | Add AZURE_SPEECH_KEY and AZURE_SPEECH_REGION to .env |
| Weather not working | Add OPENWEATHER_API_KEY to .env |
| `TemplateDoesNotExist: voice/voice_assistant.html` | Make sure templates/voice/ folder exists |
