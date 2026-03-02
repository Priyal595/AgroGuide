
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rag.api_service import ask_assistant
import json
from weather.services import fetch_weather_by_coordinates

@csrf_exempt
def assistant_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        body = json.loads(request.body)
        question = body.get("query")
        lat = body.get("lat")
        lon = body.get("lon")
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not question:
        return JsonResponse({"error": "Query is required"}, status=400)

    result = ask_assistant(question)

    climate_map = {
    "rice": (20, 35),
    "wheat": (10, 25),
    "maize": (18, 27),
    "banana": (15, 35),
    }

    crop = result.get("crop")

    if crop and crop.lower() in climate_map:
        try:
            if lat is not None and lon is not None:
                weather_data = fetch_weather_by_coordinates(lat, lon)
                current_temp = weather_data.get("temperature")

                min_temp, max_temp = climate_map[crop.lower()]

                if current_temp is not None:
                    if current_temp < min_temp:
                        advisory = "Current temperature is slightly low for this crop."
                    elif current_temp > max_temp:
                        advisory = "Temperature is high. Ensure irrigation."
                    else:
                        advisory = "Current temperature is suitable for cultivation."

                    result["current_temperature"] = current_temp
                    result["advisory"] = advisory
            else:
                result["weather_error"] = "Location not provided"

        except Exception as e:
            result["weather_error"] = str(e)

    return JsonResponse({
        "query": question,
        **result
    })