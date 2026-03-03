from django.urls import path
from .views import get_categories, get_questions, get_answer

urlpatterns = [
    path("categories/", get_categories),
    path("questions/", get_questions),
    path("answer/", get_answer),
]