from django.contrib import admin

# Register your models here.
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "nitrogen",
        "phosphorus",
        "potassium",
        "temperature",
        "humidity",
        "rainfall",
        "ph",
        "created_at",
    )
    list_filter = ("user", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
