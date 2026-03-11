# Student Cannabis Addiction Risk Prediction API

COMP3011 — Web Services and Web Data | University of Leeds 2025–2026

A Django web API that predicts cannabis addiction risk in students
using a Random Forest classifier trained on the UCI Drug Consumption
dataset (Fehrman E et al, 2015).

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/TerrenceGwati/addiction-risk-api.git
cd addiction-risk-api

### 2. Create and activate a conda environment
conda create -n addiction-risk python=3.11
conda activate addiction-risk

### 3. Install dependencies
pip install django scikit-learn pandas joblib numpy

### 4. Apply migrations
python manage.py migrate

### 5. Create an admin user
python manage.py createsuperuser

### 6. Run the server
python manage.py runserver

### 7. Open the app
- Questionnaire: http://127.0.0.1:8000/risk/
- Admin panel:   http://127.0.0.1:8000/admin/

## Dataset
UCI Drug Consumption (Quantified)
https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified
Fehrman E et al. (2015), arXiv:1506.06297

## API Documentation
See API_DOCUMENTATION.pdf in this repository.

## Tech Stack
- Django 5.2
- SQLite3
- scikit-learn (Random Forest)
- Python 3.11