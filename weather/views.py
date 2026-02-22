from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .services import fetch_weather_by_city, fetch_weather_by_coordinates


@require_http_methods(["GET"])
@login_required
def get_weather(request):

    city = request.GET.get("city")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    # If city is provided
    if city:
        try:
            weather_data = fetch_weather_by_city(city)
            return JsonResponse(weather_data)
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500
            )

    # If coordinates are provided
    if lat and lon:
        try:
            weather_data = fetch_weather_by_coordinates(lat, lon)
            return JsonResponse(weather_data)
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=500
            )

    # If neither provided
    return JsonResponse(
        {"error": "Provide either city or lat & lon"},
        status=400
    )