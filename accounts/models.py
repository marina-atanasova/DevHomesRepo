from django.db import models

from Listings.models import Property
from accounts.choices import MessageStatusChoices


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
    message = models.TextField("Message")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=MessageStatusChoices.choices,
        default=MessageStatusChoices.NEW,
    )



class Realtor(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)



