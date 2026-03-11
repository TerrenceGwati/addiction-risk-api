from django.db import models

RISK_BANDS = [
    ("low",       "Low Risk"),
    ("moderate",  "Moderate Risk"),
    ("high",      "High Risk"),
    ("very_high", "Very High Risk"),
]

class PredictionRecord(models.Model):
    created_at    = models.DateTimeField(auto_now_add=True)
    answers_json  = models.JSONField()
    risk_score    = models.FloatField()
    risk_band     = models.CharField(max_length=20, choices=RISK_BANDS)
    model_version = models.CharField(max_length=50, default="rf_cannabis_v1")

    class Meta:
        ordering = ["-created_at"]  # newest records first in querysets

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} — {self.get_risk_band_display()} ({self.risk_score:.3f})"