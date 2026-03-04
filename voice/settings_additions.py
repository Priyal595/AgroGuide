"""
════════════════════════════════════════════════════════════════
 PASTE THIS CODE AT THE VERY BOTTOM OF  AgroGuide/core/settings.py
════════════════════════════════════════════════════════════════

ALSO add 'voice' to your INSTALLED_APPS list like this:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ... your existing apps ...
    'accounts',
    'voice',          # ← ADD THIS
]
"""

import os

# ── Voice Assistant / Azure OpenAI ───────────────────────────
AZURE_OPENAI_ENDPOINT    = os.environ.get('AZURE_OPENAI_ENDPOINT',    '')
AZURE_OPENAI_API_KEY     = os.environ.get('AZURE_OPENAI_API_KEY',     '')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
AZURE_OPENAI_DEPLOYMENT  = os.environ.get('AZURE_OPENAI_DEPLOYMENT',  'gpt35')

# ── Azure Speech (TTS + STT) ──────────────────────────────────
AZURE_SPEECH_KEY         = os.environ.get('AZURE_SPEECH_KEY',    '')
AZURE_SPEECH_REGION      = os.environ.get('AZURE_SPEECH_REGION', '')

# ── OpenWeatherMap ─────────────────────────────────────────────
OPENWEATHER_API_KEY      = os.environ.get('OPENWEATHER_API_KEY', '')
