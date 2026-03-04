from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .services import fetch_weather_by_city, fetch_weather_by_coordinates
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json
from datetime import datetime


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
    if lat is not None and lon is not None:
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

    # views.py




from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import json
import base64
import io
from datetime import datetime


def download_report(request):

    if request.method != "POST":
        return HttpResponse("Only POST allowed", status=405)

    data = json.loads(request.body)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="crop_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    y = 800

    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(150, y, "Crop Recommendation Report")

    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # -------------------------
    # INPUTS SECTION
    # -------------------------

    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Input Parameters")

    y -= 20
    p.setFont("Helvetica", 11)

    inputs = data.get("inputs", {})

    for key, value in inputs.items():
        p.drawString(120, y, f"{key.capitalize()}: {value}")
        y -= 15

    # -------------------------
    # PREDICTIONS
    # -------------------------

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Top Crop Recommendations")

    y -= 20
    p.setFont("Helvetica", 11)

    rank = 1

    for crop in data.get("predictions", []):
        confidence = round(crop["confidence"] * 100, 1)

        p.drawString(
            120,
            y,
            f"{rank}. {crop['crop'].title()} — {confidence}%"
        )

        y -= 18
        rank += 1

    # -------------------------
    # EXPLANATION
    # -------------------------

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, "Explanation")

    y -= 20
    p.setFont("Helvetica", 11)

    explanation = data.get("explanation", "")

    max_chars = 90
    lines = [
        explanation[i:i + max_chars]
        for i in range(0, len(explanation), max_chars)
    ]

    for line in lines:
        p.drawString(120, y, line)
        y -= 15

    # -------------------------
    # FEATURE IMPORTANCE CHART
    # -------------------------

    feature_chart = data.get("feature_chart")

    if feature_chart:

        y -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Feature Importance")

        y -= 10

        image_data = base64.b64decode(feature_chart.split(",")[1])
        image = ImageReader(io.BytesIO(image_data))

        p.drawImage(image, 100, y - 200, width=400, height=200)

        y -= 220

    # -------------------------
    # CROP FREQUENCY CHART
    # -------------------------

    freq_chart = data.get("frequency_chart")

    if freq_chart:

        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Crop Frequency")

        y -= 10

        image_data = base64.b64decode(freq_chart.split(",")[1])
        image = ImageReader(io.BytesIO(image_data))

        p.drawImage(image, 100, y - 200, width=400, height=200)

    p.showPage()
    p.save()

    return response