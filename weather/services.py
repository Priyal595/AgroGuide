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
        raise Exception(response.text)

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    description = data["weather"][0]["description"].title()
    icon_code = data["weather"][0]["icon"]
    wind_speed = data["wind"]["speed"]

    return {
    "city": data["name"],
    "temperature": round(temperature),
    "humidity": humidity,
    "rainfall": rainfall,
    "description": description,
    "wind_speed": wind_speed,
    "icon": f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    }
def fetch_weather_by_coordinates(lat, lon):

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
    description = data["weather"][0]["description"].title()
    icon_code = data["weather"][0]["icon"]
    wind_speed = data["wind"]["speed"]
    city_name = data["name"]

    rainfall = 0
    if "rain" in data:
        rainfall = data["rain"].get("1h", 0)

    return {
        "city": data["name"],
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "description": description,
        "wind_speed": wind_speed,
        "icon": f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    }