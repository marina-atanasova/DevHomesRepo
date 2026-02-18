from django.urls import path
from .views import ContactInquiryCreateView

app_name = "accounts"

urlpatterns = [
    path("contact/", ContactInquiryCreateView.as_view(), name="contact"),
]
