from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ContactInquiryForm
from .models import UserInquiry


class ContactInquiryCreateView(CreateView):
    model = UserInquiry
    form_class = ContactInquiryForm
    template_name = "accounts/contact_form.html"
    success_url = "/listings/"

