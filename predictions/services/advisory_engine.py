def generate_modern_advisory(prediction, weather_data):
    # -----------------------------
    # 1. Soil Environmental Profile (Static)
    # -----------------------------
    profile = {
        "temperature": prediction.temperature,
        "rainfall": prediction.rainfall,
        "humidity": prediction.humidity,
        "nitrogen": prediction.nitrogen,
        "phosphorus": prediction.phosphorus,
        "potassium": prediction.potassium,
        "ph": prediction.ph,
    }

    detected_issues = []
    critical_recommendations = []
    optimization_recommendations = []

    # ------------------------------------------
    # 2. Separate Soil vs Live Climate Values
    # ------------------------------------------

    soil_temperature = profile["temperature"]
    soil_humidity = profile["humidity"]
    soil_rainfall = profile["rainfall"]

    if weather_data:
        live_temperature = weather_data.get("temperature", soil_temperature)
        live_humidity = weather_data.get("humidity", soil_humidity)
        live_rainfall = weather_data.get("rainfall", soil_rainfall)
    else:
        live_temperature = soil_temperature
        live_humidity = soil_humidity
        live_rainfall = soil_rainfall

    nitrogen = profile["nitrogen"]
    ph = profile["ph"]

    # --------------------------------------------------
    # 3. Reactive Layer (Soil-Based Critical Issues)
    # --------------------------------------------------

    # Severe Soil Moisture Stress (based on soil + heat)
    if soil_rainfall < 80 and live_temperature > 32:
        detected_issues.append("Severe Moisture Stress")

        critical_recommendations.append({
            "title": "Emergency Drip Irrigation Setup",
            "category": "Water Management",
            "reason": "Low soil rainfall combined with high temperature may severely affect crop yield.",
            "steps": [
                "Install drip irrigation immediately.",
                "Schedule early morning irrigation.",
                "Monitor soil moisture weekly."
            ],
            "benefits": [
                "Prevents crop failure",
                "Improves water efficiency",
                "Reduces evaporation loss"
            ]
        })

    # Severe pH imbalance
    if ph < 5.0 or ph > 8.0:
        detected_issues.append("Critical Soil pH Imbalance")

        critical_recommendations.append({
            "title": "Immediate Soil pH Correction",
            "category": "Soil Health",
            "reason": "Soil pH is far from optimal crop range.",
            "steps": [
                "Conduct detailed soil testing.",
                "Apply lime (for acidic soil) or gypsum (for alkaline soil).",
                "Re-test soil after amendment."
            ],
            "benefits": [
                "Restores nutrient absorption",
                "Prevents long-term soil degradation"
            ]
        })

    # --------------------------------------------------
    # 4. Live Climate-Based Reactive Advisory
    # --------------------------------------------------

    # Heatwave Detection
    if live_temperature >= 35:
        detected_issues.append("Heatwave Conditions")

        critical_recommendations.append({
            "title": "Immediate Mulching & Shade Protection",
            "category": "Climate Resilience",
            "reason": "High temperature detected from live weather data may stress crops.",
            "steps": [
                "Apply organic mulch around crop base.",
                "Use shade nets for sensitive crops.",
                "Schedule irrigation during early morning."
            ],
            "benefits": [
                "Reduces heat stress",
                "Maintains soil moisture",
                "Prevents crop damage"
            ]
        })

    # High Humidity (Fungal Risk)
    if live_humidity >= 85:
        detected_issues.append("High Humidity – Fungal Risk")

        critical_recommendations.append({
            "title": "Integrated Pest & Fungal Management",
            "category": "Crop Protection",
            "reason": "High humidity increases fungal infection probability.",
            "steps": [
                "Improve field ventilation.",
                "Avoid over-irrigation.",
                "Use bio-fungicides where necessary."
            ],
            "benefits": [
                "Prevents crop disease",
                "Improves plant health",
                "Reduces yield loss"
            ]
        })

    # Heavy Rainfall Alert
    if live_rainfall >= 300:
        detected_issues.append("Excess Rainfall Risk")

        critical_recommendations.append({
            "title": "Field Drainage Optimization",
            "category": "Water Management",
            "reason": "Heavy rainfall may cause waterlogging.",
            "steps": [
                "Ensure proper field drainage channels.",
                "Avoid standing water accumulation.",
                "Monitor root oxygen levels."
            ],
            "benefits": [
                "Prevents root rot",
                "Improves soil aeration"
            ]
        })

    # --------------------------------------------------
    # 5. Optimization Layer (Always Suggest)
    # --------------------------------------------------

    # Water Strategy
    if soil_rainfall < 150:
        water_strategy = {
            "title": "Drip Irrigation System",
            "category": "Water Optimization",
            "reason": "Soil rainfall levels suggest efficient irrigation can improve yield stability.",
            "steps": [
                "Design irrigation layout based on crop spacing.",
                "Install mainline and lateral pipes.",
                "Place emitters near root zones.",
                "Maintain filtration system regularly."
            ],
            "benefits": [
                "Saves 30–70% water",
                "Improves yield consistency",
                "Reduces fertilizer loss"
            ]
        }
    else:
        water_strategy = {
            "title": "Rainwater Harvesting System",
            "category": "Water Optimization",
            "reason": "Higher rainfall regions benefit from structured water conservation systems.",
            "steps": [
                "Construct water storage tanks.",
                "Install runoff collection channels.",
                "Reuse stored water during dry periods."
            ],
            "benefits": [
                "Improves water availability",
                "Reduces dependency on groundwater"
            ]
        }

    optimization_recommendations.append(water_strategy)

    # Soil Strategy
    if nitrogen < 50:
        soil_strategy = {
            "title": "Organic Composting & Green Manuring",
            "category": "Soil Optimization",
            "reason": "Nitrogen levels indicate opportunity for soil enrichment.",
            "steps": [
                "Prepare compost pit.",
                "Incorporate organic waste and manure.",
                "Apply before sowing season."
            ],
            "benefits": [
                "Improves soil fertility",
                "Enhances microbial activity",
                "Long-term sustainability"
            ]
        }
    else:
        soil_strategy = {
            "title": "Precision Fertigation",
            "category": "Soil Optimization",
            "reason": "Balanced nutrients allow advanced precision nutrient delivery.",
            "steps": [
                "Install fertigation unit.",
                "Calibrate nutrient dosing schedule.",
                "Monitor nutrient levels monthly."
            ],
            "benefits": [
                "Optimized fertilizer usage",
                "Improved crop productivity"
            ]
        }

    optimization_recommendations.append(soil_strategy)

    # Climate Resilience Strategy
    climate_strategy = {
        "title": "Mulching & Crop Residue Management",
        "category": "Climate Resilience",
        "reason": "Temperature variation requires soil moisture stabilization techniques.",
        "steps": [
            "Apply organic mulch layer.",
            "Maintain 5–8 cm thickness.",
            "Retain crop residues post-harvest."
        ],
        "benefits": [
            "Reduces evaporation",
            "Improves soil structure",
            "Prevents weed growth"
        ]
    }

    optimization_recommendations.append(climate_strategy)

    # Precision Technology Strategy
    precision_strategy = {
        "title": "Smart Soil & Irrigation Monitoring",
        "category": "Precision Agriculture",
        "reason": "Modern farming benefits from data-driven decision making.",
        "steps": [
            "Install soil moisture sensors.",
            "Use automated irrigation scheduling.",
            "Track environmental data weekly."
        ],
        "benefits": [
            "Improves efficiency",
            "Reduces resource wastage",
            "Increases long-term yield"
        ]
    }

    optimization_recommendations.append(precision_strategy)

    # --------------------------------------------------
    # 6. Final Structured Output
    # --------------------------------------------------

    return {
        "profile": profile,
        "detected_issues": detected_issues,
        "critical_recommendations": critical_recommendations,
        "optimization_recommendations": optimization_recommendations
    }