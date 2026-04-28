from django.test import TestCase

from django.test import TestCase, Client
from .ml_utils import compute_risk_score

class RiskScoreTests(TestCase):
    def test_high_risk_profile_returns_very_high(self):
        inputs = {
        'Nscore': 0.5, 'Escore': 0.3, 'Oscore': 1.2,
        'Ascore': -0.5, 'Cscore': -1.5, 'Impulsive': 1.8,
        'SS': 1.9, 'Age': -0.5, 'Gender': 0.5,
        'Education': -0.6, 'Country': 0.5, 'Ethnicity': -0.3
        }
        score, band = compute_risk_score(inputs)
        self.assertGreater(score, 0.75)
        self.assertEqual(band, "very_high")

    def test_low_risk_profile_returns_low(self):
        inputs = {
        'Nscore': -0.5, 'Escore': 0.1, 'Oscore': -1.2,
        'Ascore': 1.0, 'Cscore': 1.5, 'Impulsive': -1.5,
        'SS': -1.8, 'Age': 0.5, 'Gender': 0.5,
        'Education': 0.6, 'Country': 0.5, 'Ethnicity': -0.3
        }
        score, band = compute_risk_score(inputs)
        self.assertLess(score, 0.30)
        self.assertEqual(band, "low")

class ViewTests(TestCase):
    def test_risk_page_loads(self):
        client = Client()
        response = client.get('/risk/')
        self.assertEqual(response.status_code, 200)
