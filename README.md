# AgroGuide 🌱  
### Smart AI-Powered Crop Recommendation Platform

AgroGuide is an AI-powered smart farming advisory platform that helps farmers choose the most suitable crops based on soil nutrients and environmental conditions.

The system combines machine learning, real-time weather data, agricultural knowledge, and AI assistants to provide intelligent farming guidance.

---

# Key Features

## ML-Based Crop Recommendation
AgroGuide predicts the most suitable crops using:

Soil Parameters
- Nitrogen
- Phosphorus
- Potassium
- pH

Environmental Factors
- Temperature
- Humidity
- Rainfall

The system returns the **top 3 recommended crops** along with confidence scores.

---

## Explainable AI
AgroGuide provides **feature importance visualization** showing how each environmental parameter affects the prediction.

---

## Smart Farming Advisor
The platform suggests strategies to improve farming practices such as:

- Precision fertilization
- Rainwater harvesting
- Mulching techniques
- Soil monitoring strategies

---

## Real-Time Weather Integration
Weather API automatically fetches environmental data such as:

- Temperature
- Humidity
- Weather conditions

This improves prediction accuracy by using real-time climate data.

---

## Agriculture News Feed
AgroGuide integrates a News API to display the latest updates in agriculture including:

- Agricultural technology
- Crop innovations
- Government farming policies
- Market trends

---

## Smart Chatbot
A built-in AI chatbot helps farmers by answering queries related to:

- Soil nutrients
- Crop cultivation techniques
- Agricultural practices

---

## Multilingual Voice Assistant
Farmers can interact with the system using voice or text queries, currently available in 5 different language.

The voice assistant provides responses for:

- Government schemes
- Crop information (40+ crops)
- Farming methods and techniques

---

## User Dashboard
The dashboard provides an interactive interface including:

- Soil input sliders
- Crop prediction results
- Feature importance charts
- Prediction history

# Prediction Workflow

1. User enters soil parameters (N, P, K, pH).  
2. Weather API fetches climate data automatically.  
3. Backend validates input data.  
4. ML model generates crop prediction.  
5. Top recommended crops are displayed.  
6. Feature importance explains prediction.


## Setup Instructions (Development)

1. Create virtual environment
```bash
python -m venv venv
```
2. Activate environment
 ```bash
Windows: venv\Scripts\activate  
Linux/Mac: source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run migrations
 ```bash
python manage.py migrate
```
5. Start server
```bash
python manage.py runserver
```
---

---



## Maintained By
AgroGuide Team 🌱


