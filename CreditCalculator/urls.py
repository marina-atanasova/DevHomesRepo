from django.urls import path
from . import views
from .views import DeleteCreditRequest

app_name = "CreditCalculator"

urlpatterns = [
    path("credit/", views.calculator_view, name="credit"),
    path("credit/all/", views.AllCreditRequests.as_view(), name="credit_all"),
    path("credit/<int:pk>/delete", DeleteCreditRequest.as_view(), name="credit_delete"),
]