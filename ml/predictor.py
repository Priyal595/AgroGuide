import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "crop_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "features.pkl"))

FEATURE_NAME_MAP = {
    "N": "Nitrogen",
    "P": "Phosphorus",
    "K": "Potassium",
    "temperature": "Temperature",
    "humidity": "Humidity",
    "ph": "Soil pH",
    "rainfall": "Rainfall"
}

def predict_crop(input_data):
    """
    input_data: dict with keys
    N, P, K, temperature, humidity, ph, rainfall
    """

    input_list = [input_data[feature] for feature in features]
    input_array = np.array(input_list).reshape(1, -1)

    probabilities = model.predict_proba(input_array)[0]
    classes = model.classes_

    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    top_3_predictions = [
        {
            "crop": classes[i],
            "confidence": round(float(probabilities[i]), 3)
        }
        for i in top_3_idx
    ]

    importances = model.feature_importances_
    feature_importance = sorted(
        [
            {
                "feature": FEATURE_NAME_MAP.get(features[i], features[i]),
                "importance": round(float(importances[i]), 3)
            }
            for i in range(len(features))
        ],
        key=lambda x: x["importance"],
        reverse=True
    )

    return {
        "top_3_crops": top_3_predictions,
        "feature_importance": feature_importance
    }