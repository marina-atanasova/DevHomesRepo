from django.db import models

# Create your models here.
class Property(models.Model):
    address = models.CharField("Address", max_length=255)
    size = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
