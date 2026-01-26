from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Prediction



@csrf_exempt            
@login_required         
def predict_crop(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method is allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    
    required_fields = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "temperature",
        "humidity",
        "rainfall",
        "ph",
    ]

    # Validate required fields
    for field in required_fields:
        if field not in data:
            return JsonResponse(
                {"error": f"Missing field: {field}"},
                status=400
            )

        if not isinstance(data[field], (int, float)):
            return JsonResponse(
                {"error": f"{field} must be a number"},
                status=400
            )
    
    # -------------------------------
    # DUMMY RESPONSE (NO ML YET)
    # -------------------------------
    response = {
        "predictions": [
            {"name": "Rice", "score": 0.89},
            {"name": "Wheat", "score": 0.76},
            {"name": "Maize", "score": 0.68},
        ],
        "explanation": "Rice is recommended due to high nitrogen and adequate rainfall.",
        "feature_importance": {
            "labels": [
                "Nitrogen",
                "Phosphorus",
                "Potassium",
                "Temperature",
                "Humidity",
                "Rainfall",
                "pH",
            ],
            "values": [0.25, 0.18, 0.15, 0.14, 0.12, 0.10, 0.06],
        },
    }

    
    Prediction.objects.create(
        user=request.user,
        nitrogen=data["nitrogen"],
        phosphorus=data["phosphorus"],
        potassium=data["potassium"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        rainfall=data["rainfall"],
        ph=data["ph"],
        result=response
    )
    return JsonResponse(response)



