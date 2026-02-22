import requests
from django.conf import settings


def fetch_weather_by_city(city):
    api_key = settings.OPENWEATHER_API_KEY

    if not api_key:
        raise Exception("Weather API key not configured")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch weather data")

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
    }
def fetch_weather_by_coordinates(lat, lon):
    import requests
    from django.conf import settings

    api_key = settings.OPENWEATHER_API_KEY

    if not api_key:
        raise Exception("Weather API key not configured")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"OpenWeather error: {response.text}")

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
    }