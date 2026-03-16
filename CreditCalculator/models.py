from django.db import models

from Listings.models import Property


# Create your models here.

class CreditRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    property_price = models.FloatField()
    interest_rate = models.FloatField()
    down_payment = models.IntegerField()
    repayment_years = models.IntegerField()
    linked_property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_requests'
    )

    def __str__(self):
        return f"Credit request {self.created_at:%Y-%m-%d}"
