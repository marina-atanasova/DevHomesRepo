from django.db import models

from Listings.models import Property
from accounts.choices import MessageStatusChoices, RequestTypeChoices


# Create your models here.

class UserInquiry(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    listing = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries",
    )
    request_type = models.CharField(
        choices=RequestTypeChoices.choices,
        default=RequestTypeChoices.OTHER
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=MessageStatusChoices.choices,
        default=MessageStatusChoices.NEW,
    )
    reply_message = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)



