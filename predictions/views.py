from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Prediction
from ml.predictor import predict_crop as ml_predict_crop


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
    # REAL ML PREDICTION
    # -------------------------------
    input_data = {
        "N": data["nitrogen"],
        "P": data["phosphorus"],
        "K": data["potassium"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "rainfall": data["rainfall"],
        "ph": data["ph"],
    }

    ml_result = ml_predict_crop(input_data)

    # -------------------------------
    # SAVE TO DATABASE
    # -------------------------------
    Prediction.objects.create(
        user=request.user,
        nitrogen=data["nitrogen"],
        phosphorus=data["phosphorus"],
        potassium=data["potassium"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        rainfall=data["rainfall"],
        ph=data["ph"],
        result=ml_result
    )

    # -------------------------------
    # RETURN RESPONSE
    # -------------------------------
    return JsonResponse({
        "predictions": ml_result["top_3_crops"],
        "feature_importance": ml_result["feature_importance"]
    })


@login_required
def prediction_history(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    data = []
    for p in predictions:
        data.append({
            "id": p.id,
            "inputs": {
                "nitrogen": p.nitrogen,
                "phosphorus": p.phosphorus,
                "potassium": p.potassium,
                "temperature": p.temperature,
                "humidity": p.humidity,
                "rainfall": p.rainfall,
                "ph": p.ph,
            },
            "result": p.result,
            "created_at": p.created_at.isoformat(),
        })

    return JsonResponse({"history": data})