from django.shortcuts import render
from django.contrib import messages

from .ml_utils import compute_risk_score, FEATURE_COLUMNS
from .models import PredictionRecord

def risk_form(request):
    if request.method == "POST":
        # ── Parse demographic dropdowns (pre-mapped UCI float values) ─────────
        # These come straight from the form option value attributes
        # e.g. Age "18-24" → "-0.95197" already set in the HTML
        try:
            clean = {col: float(request.POST[col]) for col in FEATURE_COLUMNS}
        except (KeyError, ValueError):
            # A field was missing or non-numeric — re-render the form with error
            messages.error(request, "Please complete all fields before submitting.")
            return render(request, "riskapp/form.html")

        # ── Run prediction ────────────────────────────────────────────────────
        risk_score, risk_band = compute_risk_score(clean)

        # ── Persist result ────────────────────────────────────────────────────
        PredictionRecord.objects.create(
            answers_json=clean,
            risk_score=risk_score,
            risk_band=risk_band,
        )

        context = {
            "risk_score": risk_score,   # passed as float — result.html uses |floatformat:3
            "risk_band":  risk_band,
        }
        return render(request, "riskapp/result.html", context)

    # GET — render blank form
    return render(request, "riskapp/form.html")