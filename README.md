# AgroGuide 🌾  
Crop Recommendation System

AgroGuide is a web-based application that recommends the most suitable crops based on soil nutrients and climatic conditions using machine learning.

---

## Project Structure

![Project Folder Structure](images/folder_structure.png)

## Current Project Status ✅

### Completed
- Frontend UI (All pages)
- Authentication flow (Register, Login, Logout)
- Email verification (console-based for development)
- Dashboard UI with sliders, charts, and result sections
- Prediction API endpoint (dummy / rule-based response)
- Prediction data storage in database
- API integration with dashboard
- Prediction history API (data fetching works)

### In Progress
- Dashboard history UI rendering (backend data already available)
- ML model integration with prediction API
- Improving explanation logic based on ML output

### Pending
- Replace dummy logic with trained ML model
- Real email SMTP setup (production)
- Feature importance from actual ML model
- Performance tuning & validations

---

## Frontend Status (COMPLETED – DO NOT MODIFY)

The frontend is fully implemented and stable.

### Pages
- Landing Page
- Login Page
- Register Page
- Email Verification Status Page (verify_status.html)
- Dashboard (Sliders, Charts, Results, History Section)

### JavaScript Logic
- slider.js – Handles sliders & input values
- dashboard.js – Form submission, API calls & results rendering
- charts.js – Chart.js visualizations

Frontend expects strict backend response formats.

---

## Backend Responsibilities 🚀

Backend developers should focus ONLY on the following areas:

---

### 1. API Endpoint: Crop Prediction

URL  
POST /api/predict/

Current Status:
- API exists and works
- Data is stored in DB
- Dummy / placeholder prediction logic is used

To Do:
- Integrate ML model
- Replace dummy predictions with real output

Expected JSON Request
{
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "temperature": 25.5,
  "humidity": 80,
  "rainfall": 200,
  "ph": 6.5
}

Expected JSON Response
{
  "predictions": [
    { "name": "Rice", "score": 0.89 },
    { "name": "Wheat", "score": 0.76 },
    { "name": "Maize", "score": 0.68 }
  ],
  "explanation": "Rice is recommended due to high nitrogen and adequate rainfall.",
  "feature_importance": {
    "labels": ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "Rainfall", "pH"],
    "values": [0.25, 0.18, 0.15, 0.14, 0.12, 0.10, 0.06]
  }
}

IMPORTANT
- score must be between 0 and 1
- feature importance values must sum to 1
- response structure must not change

---

### 2. Prediction History

Current Status:
- Prediction data is saved per user
- History API endpoint works

To Do:
- Ensure consistent data formatting
- Improve ordering & pagination if needed

---

### 3. URL Names (DO NOT CHANGE)

These URL names are already used in templates and JavaScript.

| URL Name | Purpose |
| landing | Home page |
| login | Login page |
| register | Registration page |
| dashboard | User dashboard |
| logout | Logout |
| verify_email | Email verification |

Changing these WILL break the frontend.

---

### 4. Email Verification (Development Setup)

Current Setup:
- Console email backend is enabled
- Verification email is printed in terminal

Verification Flow:
1. User registers
2. Verification link is printed in terminal
3. User copies the link
4. Opens it in browser
5. Account gets activated

This is intentional for development/testing.

Production To Do:
- Configure SMTP
- Move email credentials to .env
- Switch email backend

---

### 5. Authentication

- Django default User model is used
- Email-based login (mapped internally to username)
- User must verify email before accessing dashboard
- Login redirects to dashboard on success

---

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

## Notes for Contributors

- Frontend is complete – do not change without discussion
- Backend APIs must follow exact response formats
- ML integration is the primary remaining task
- Email is console-based by design for now

---

## Maintained By
AgroGuide Team 🌱


