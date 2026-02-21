from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from .forms import ContactInquiryForm, ContactForm
from .models import UserInquiry


class ContactInquiryCreateView(CreateView):
    model = UserInquiry
    form_class = ContactInquiryForm
    template_name = "accounts/contact_form.html"
    success_url = reverse_lazy("accounts:contact-dashboard")


class ContactInquiryUpdateView(UpdateView):
    model = UserInquiry
    form_class = ContactForm
    template_name = "accounts/contact_edit.html"
    success_url = reverse_lazy("accounts:contact-dashboard")


class ContactInquiryListView(ListView):
    model = UserInquiry
    template_name = "accounts/contact_dashboard.html"
    context_object_name = "inquiries"
    ordering = ['-created_at']



class ContactInquiryDetailView(DetailView):
    model = UserInquiry
    template_name = "accounts/contact_details.html"

class ContactInquiryDeleteView(DeleteView):
    model = UserInquiry
    template_name = "accounts/contact_delete_confirm.html"
    success_url = reverse_lazy("accounts:contact-dashboard")
