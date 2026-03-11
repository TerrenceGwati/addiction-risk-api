import os
import joblib
import pandas as pd
from django.conf import settings

# ── Load model ────────────────────────────────────────────────────────────────
# Random Forest does not require a scaler — tree-based models split on
# feature thresholds, not distances or gradients, so raw UCI values are passed
# directly. Do NOT scale the input or predictions will be wrong.

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_artifacts", "rf_cannabis_model.joblib")

rf_model = joblib.load(MODEL_PATH)

# ── Feature order — MUST match training column order exactly ──────────────────
FEATURE_COLUMNS = [
    "Age",
    "Gender",
    "Education",
    "Country",
    "Ethnicity",
    "Nscore",
    "Escore",
    "Oscore",
    "Ascore",
    "Cscore",
    "Impulsive",
    "SS",
]

# ── Risk tier thresholds ───────────────────────────────────────────────────────
# Boundaries tuned to the Random Forest's probability range.
# Model trained at threshold=0.45 to maximise recall for at-risk students.
# A false negative (missed at-risk student) is costlier than a false positive.
#
# Tier        Range              Action
# ---------   -----------------  ---------------------------------------------
# Low         prob < 0.30        No immediate concern
# Moderate    0.30 – 0.55        Worth monitoring; suggest wellbeing resources
# High        0.55 – 0.75        Counselling referral advised
# Very High   prob >= 0.75       Prioritise urgent intervention

LOW_CUT      = 0.30
MODERATE_CUT = 0.55
HIGH_CUT     = 0.75


def band_from_proba(p: float) -> str:
    if   p < LOW_CUT:      return "low"
    elif p < MODERATE_CUT: return "moderate"
    elif p < HIGH_CUT:     return "high"
    else:                  return "very_high"


def compute_risk_score(clean_input_dict: dict) -> tuple[float, str]:
    """
    Predict cannabis addiction risk from a student's questionnaire responses.

    Parameters
    ----------
    clean_input_dict : dict
        Maps each feature name to its UCI-quantified value.
        Demographic fields (Age, Gender, Education, Country, Ethnicity) should
        be the pre-mapped float values from the form dropdowns.
        Personality fields (Nscore, Escore, Oscore, Ascore, Cscore, Impulsive,
        SS) should be the UCI-mapped values from the slider hidden fields.
        All 12 keys in FEATURE_COLUMNS must be present.

    Returns
    -------
    risk_score : float
        Probability of cannabis addiction risk (0.0 – 1.0).
    risk_band  : str
        One of: 'low', 'moderate', 'high', 'very_high'

    Example
    -------
    >>> answers = {
    ...     "Age":       -0.95197,   # 18-24
    ...     "Gender":    -0.48246,   # Male
    ...     "Education":  1.98437,   # Doctorate
    ...     "Country":    0.96082,   # UK
    ...     "Ethnicity": -0.31685,   # Mixed-White/Asian
    ...     "Nscore":     0.84580,   # High neuroticism
    ...     "Escore":    -0.30172,   # Low extraversion
    ...     "Oscore":     1.43533,   # High openness
    ...     "Ascore":    -0.80615,   # Low agreeableness
    ...     "Cscore":    -0.01928,   # Average conscientiousness
    ...     "Impulsive":  0.59042,   # Above-average impulsivity
    ...     "SS":         1.30612,   # High sensation-seeking
    ... }
    >>> score, band = compute_risk_score(answers)
    >>> print(score, band)
    0.905 very_high
    """
    # Build a named DataFrame — Random Forest was fitted with feature names
    # so passing a DataFrame avoids the "X does not have valid feature names"
    # UserWarning that occurs when a plain numpy array is passed instead.
    x = pd.DataFrame([clean_input_dict])[FEATURE_COLUMNS]

    # Get probability for class 1 (At Risk)
    # No scaling step — Random Forest does not require StandardScaler
    risk_score = float(rf_model.predict_proba(x)[0, 1])
    risk_band  = band_from_proba(risk_score)

    return risk_score, risk_band