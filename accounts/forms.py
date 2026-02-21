from django import forms
from django.utils import timezone

from .choices import MessageStatusChoices
from .models import UserInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = UserInquiry
        fields = ["first_name", "last_name", "email", "phone", "listing", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class ContactForm(forms.ModelForm):
    class Meta:
        model = UserInquiry
        fields = "__all__"
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
            # Optional: make reply_message bigger too
            "reply_message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "created_at" in self.fields:
            self.fields["created_at"].disabled = True  # real read-only

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.status == MessageStatusChoices.CLOSED:
            if not instance.closed_at:
                instance.closed_at = timezone.now()
        else:
            instance.closed_at = None

        if commit:
            instance.save()
            self.save_m2m()
        return instance