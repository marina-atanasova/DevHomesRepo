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
            "reply_message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "created_at" in self.fields:
            self.fields["created_at"].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        reply_text = (instance.reply_message or "").strip()
        if instance.status == MessageStatusChoices.NEW:
            instance.status = MessageStatusChoices.IN_PROGRESS

        if reply_text:
            instance.replied_at = timezone.now()
        else:
            instance.replied_at = None

        if instance.status == MessageStatusChoices.CLOSED:
            instance.closed_at = timezone.now()
        else:
            instance.closed_at = None

        if commit:
            instance.save()
            self.save_m2m()
        return instance