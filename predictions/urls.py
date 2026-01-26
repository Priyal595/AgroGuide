from django.urls import path
from .views import predict_crop, prediction_history

urlpatterns = [
    path("predict/", predict_crop, name="predict"),
    path("history/", prediction_history, name="prediction_history"),
]
