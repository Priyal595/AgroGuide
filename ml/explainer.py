def generate_explanation(input_data, top_crop, feature_importance):
    """
    Generates a human-readable explanation
    """

    reasons = []

    rainfall = input_data["rainfall"]
    temperature = input_data["temperature"]
    ph = input_data["ph"]

    #---------------------------------------------------------------------------------------
    # Rainfall reasoning
    #---------------------------------------------------------------------------------------
    if rainfall > 150:
        reasons.append("high rainfall conditions")
    elif rainfall < 60:
        reasons.append("low rainfall conditions")
    else:
        reasons.append("moderate rainfall levels")

    # Temperature reasoning
    if 20 <= temperature <= 30:
        reasons.append("optimal temperature range")
    elif temperature > 35:
        reasons.append("high temperature conditions")

    # Soil pH reasoning
    if 6 <= ph <= 7.5:
        reasons.append("near-neutral soil pH ideal for nutrient absorption")
    elif ph < 5.5:
        reasons.append("acidic soil conditions")

    # Most important feature
    if feature_importance:
        top_feature = feature_importance[0]["feature"]
        reasons.append(f"{top_feature} being a key influencing factor")

    explanation = (
        f"{top_crop} is recommended due to "
        + ", ".join(reasons)
        + ". These conditions align well with its growth requirements."
    )

    return explanation
