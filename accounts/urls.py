from django.urls import path
from .views import (
    ContactInquiryCreateView,
    ContactInquiryListView,
    ContactInquiryDetailView,
    ContactInquiryUpdateView,
    ContactInquiryDeleteView,
)

app_name = "accounts"

urlpatterns = [
    path("contact/", ContactInquiryCreateView.as_view(), name="contact"),
    path("contact/dashboard/", ContactInquiryListView.as_view(), name="contact-dashboard"),
    path("contact/<int:pk>/detail/", ContactInquiryDetailView.as_view(), name="contact-detail"),
    path("contact/<int:pk>/edit/", ContactInquiryUpdateView.as_view(), name="contact-edit"),
    path("contact/<int:pk>/delete/", ContactInquiryDeleteView.as_view(), name="contact-delete"),
]