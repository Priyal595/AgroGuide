from django.urls import path
from .views import predict_crop, prediction_history
from . import views
from .news_views import agro_news

urlpatterns = [
    path("predict/", predict_crop, name="predict"),
    path("history/", prediction_history, name="prediction_history"),
    path("insights/", views.user_insights, name="insights"),
    path("history/<int:pk>/", views.delete_prediction, name="delete_prediction"),
    path("history/reset/", views.reset_history, name="reset_history"),
    path("news/", agro_news, name="agro_news"),

]
