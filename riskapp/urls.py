from django.urls import path
from . import views

app_name = "riskapp"

urlpatterns = [
    path("", views.risk_form, name="form"),
]