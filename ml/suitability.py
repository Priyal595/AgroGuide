def analyze_suitability(input_data):
    """
    Returns structured suitability breakdown
    """

    analysis = {}

    # Rainfall
    rainfall = input_data["rainfall"]
    if 100 <= rainfall <= 200:
        status, level = "Ideal", "good"
    elif 60 <= rainfall < 100 or 200 < rainfall <= 250:
        status, level = "Acceptable", "moderate"
    else:
        status, level = "Low Suitability", "poor"

    analysis["Rainfall"] = {
        "status": status,
        "level": level,
        "value": f"{rainfall} mm"
    }

    # Temperature
    temp = input_data["temperature"]
    if 20 <= temp <= 30:
        status, level = "Optimal", "good"
    elif 15 <= temp < 20 or 30 < temp <= 35:
        status, level = "Moderate", "moderate"
    else:
        status, level = "High Risk", "poor"

    analysis["Temperature"] = {
        "status": status,
        "level": level,
        "value": f"{temp} °C"
    }

    # Soil pH
    ph = input_data["ph"]
    if 6 <= ph <= 7.5:
        status, level = "Balanced", "good"
    elif 5.5 <= ph < 6 or 7.5 < ph <= 8:
        status, level = "Slightly Off", "moderate"
    else:
        status, level = "Unsuitable", "poor"

    analysis["Soil pH"] = {
        "status": status,
        "level": level,
        "value": ph
    }

    # Nitrogen
    nitrogen = input_data["N"]
    if nitrogen >= 80:
        status, level = "Sufficient", "good"
    elif 50 <= nitrogen < 80:
        status, level = "Moderate", "moderate"
    else:
        status, level = "Low", "poor"

    analysis["Nitrogen"] = {
        "status": status,
        "level": level,
        "value": f"{nitrogen} kg/ha"
    }

    return analysis
