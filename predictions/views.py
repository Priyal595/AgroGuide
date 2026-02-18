from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Prediction
from ml.predictor import predict_crop as ml_predict_crop

from collections import Counter
from django.db.models import Avg

from ml.explainer import generate_explanation
from ml.suitability import analyze_suitability

from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
@require_http_methods(["DELETE"])
@login_required
def delete_prediction(request, pk):
    prediction = get_object_or_404(
        Prediction,
        id=pk,
        user=request.user
    )
    prediction.delete()

    return JsonResponse({"message": "Deleted successfully"})


@require_http_methods(["DELETE"])
@login_required
def reset_history(request):
    Prediction.objects.filter(user=request.user).delete()
    return JsonResponse({"message": "All history cleared"})




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

    # ml_result = ml_predict_crop(input_data)

    # # -------------------------------
    # # SAVE TO DATABASE
    # # -------------------------------
    # Prediction.objects.create(
    #     user=request.user,
    #     nitrogen=data["nitrogen"],
    #     phosphorus=data["phosphorus"],
    #     potassium=data["potassium"],
    #     temperature=data["temperature"],
    #     humidity=data["humidity"],
    #     rainfall=data["rainfall"],
    #     ph=data["ph"],
    #     result=ml_result
    # )

    # # -------------------------------
    # # RETURN RESPONSE
    # # -------------------------------
    
    ml_result = ml_predict_crop(input_data)

    # -------------------------------
    # FORMAT FEATURE IMPORTANCE
    # -------------------------------
    raw_importance = ml_result["feature_importance"]

    labels = [item["feature"] for item in raw_importance]
    values = [item["importance"] for item in raw_importance]

    # -------------------------------
    # GENERATE EXPLANATION
    # -------------------------------
    from ml.explainer import generate_explanation

    top_crop = ml_result["top_3_crops"][0]["crop"]

    explanation = generate_explanation(
        input_data,
        top_crop,
        raw_importance
    )
    # -------------------------------
    # GENERATE SUITABILITY ANALYSIS
    # -------------------------------

    suitability_analysis = analyze_suitability(input_data)


    # -------------------------------
    # FINAL RESPONSE STRUCTURE
    # -------------------------------
    response_data = {
        "predictions": ml_result["top_3_crops"],
        "feature_importance": {
            "labels": labels,
            "values": values
        },
        "explanation": explanation,
        "suitability_analysis": suitability_analysis
    }

    

    # SAME structure to DB
    Prediction.objects.create(
        user=request.user,
        nitrogen=data["nitrogen"],
        phosphorus=data["phosphorus"],
        potassium=data["potassium"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        rainfall=data["rainfall"],
        ph=data["ph"],
        result=response_data
    )

    # Return SAME structure to frontend
    return JsonResponse(response_data)



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



@login_required
def user_insights(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET method is allowed"},
            status=405
        )

    predictions = Prediction.objects.filter(user=request.user)

    if not predictions.exists():
        return JsonResponse({
            "total_predictions": 0,
            "most_recommended_crop": None,
            "crop_frequency": {},
            "confidence_distribution": {
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "average_conditions": {}
        })

    # 1️⃣ Total predictions
    total_predictions = predictions.count()

    # 2️⃣ Crop frequency
    top_crops = [
        p.result["predictions"][0]["crop"]
        for p in predictions
    ]
    crop_counter = Counter(top_crops)
    crop_frequency = dict(crop_counter)

    most_recommended_crop = crop_counter.most_common(1)[0][0]

    # 3️⃣ Confidence distribution
    high = 0
    medium = 0
    low = 0

    for p in predictions:
        confidence = p.result["predictions"][0]["confidence"]

        if confidence >= 0.7:
            high += 1
        elif confidence >= 0.4:
            medium += 1
        else:
            low += 1

    confidence_distribution = {
        "high": high,
        "medium": medium,
        "low": low
    }

    # 4️⃣ Average environmental conditions
    averages = predictions.aggregate(
        avg_rainfall=Avg("rainfall"),
        avg_temperature=Avg("temperature"),
        avg_ph=Avg("ph"),
        avg_humidity=Avg("humidity"),
    )

    average_conditions = {
        "rainfall": round(averages["avg_rainfall"], 2),
        "temperature": round(averages["avg_temperature"], 2),
        "ph": round(averages["avg_ph"], 2),
        "humidity": round(averages["avg_humidity"], 2),
    }

    return JsonResponse({
        "total_predictions": total_predictions,
        "most_recommended_crop": most_recommended_crop,
        "crop_frequency": crop_frequency,
        "confidence_distribution": confidence_distribution,
        "average_conditions": average_conditions,
    })
