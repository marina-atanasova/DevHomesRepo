from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from .choices import MessageStatusChoices
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

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")

        if status in {choice[0] for choice in MessageStatusChoices.choices}:
            qs = qs.filter(status=status)

        if not status:
            qs = qs.exclude(status=MessageStatusChoices.CLOSED)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_status"] = self.request.GET.get("status", "")
        ctx["status_choices"] = MessageStatusChoices.choices
        return ctx

class ContactInquiryDetailView(DetailView):
    model = UserInquiry
    template_name = "accounts/contact_details.html"

class ContactInquiryDeleteView(DeleteView):
    model = UserInquiry
    template_name = "accounts/contact_delete_confirm.html"
    success_url = reverse_lazy("accounts:contact-dashboard")
