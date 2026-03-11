from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PredictionRecord

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "risk_band", "risk_score", "model_version")
    list_filter = ("risk_band", "model_version")
    ordering = ("-created_at",)
