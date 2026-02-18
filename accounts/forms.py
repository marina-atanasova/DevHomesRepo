from django import forms
from .models import UserInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = UserInquiry
        fields = ["first_name","last_name", "email", "phone", "listing", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
