from decimal import Decimal, ROUND_HALF_UP
from random import choices

from django.contrib.postgres.fields import ArrayField
from django.db import models

from Listings.choices import CityChoices, DistrictChoices, PropertyTypeChoices, BuildTypeChoices, HeatingTypeChoices, \
    AptExposureChoices


# Create your models here.


class City(models.Model):
    name = models.CharField(
        max_length=50,
        choices=CityChoices.choices,
        default=CityChoices.SOFIA,
        unique=True
    )

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(
        max_length=50,
        choices=DistrictChoices.choices,
        default=DistrictChoices.OTHER
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')



    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["city", "name"],
                name="uniq_district_name_per_city",
            )
        ]
        ordering = ["city__name", "name"]

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField("Address", max_length=255)
    size = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    bedrooms = models.PositiveIntegerField(default=0)
    rooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    balconies = models.PositiveIntegerField(default=0)

    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="properties")
    property_type = models.CharField(max_length=255,
        choices = PropertyTypeChoices.choices,
        default= PropertyTypeChoices.Other

    )
    build_year = models.PositiveIntegerField(default=0)
    build_type = models.CharField(max_length=255,
                                  choices=BuildTypeChoices.choices,
                                  default=BuildTypeChoices.Other
                                  )
    description = models.TextField(blank=True, null=True)
    heating = models.CharField(max_length=255,
                               choices=HeatingTypeChoices.choices,
                               default=HeatingTypeChoices.Other)
    exposure = ArrayField(
        base_field=models.CharField(max_length=1, choices=AptExposureChoices.choices),
        default=list,
        blank=True,
    )
    floor = models.CharField(max_length=255, default=0)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")

    @property
    def price_per_sqm(self):
        if not self.size or not self.price:
            return None
        try:
            value = self.price / Decimal(self.size)
            return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (ZeroDivisionError, TypeError):
            return None

