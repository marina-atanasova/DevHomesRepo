from django.urls import path
from . import views

app_name = "CreditCalculator"

urlpatterns = [
    path("credit/", views.calculator_view, name="credit"),
]