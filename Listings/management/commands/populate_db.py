import random

from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import District, Property, Amenity
from Listings.choices import (
    PropertyTypeChoices,
    BuildTypeChoices,
    HeatingTypeChoices,
    AptExposureChoices,
)


class Command(BaseCommand):
    help = "Populate DB with sample properties using already-seeded cities/districts."

    @transaction.atomic
    def handle(self, *args, **options):
        # Optional: clear existing properties so reruns are clean
        Property.objects.all().delete()

        districts = list(District.objects.select_related("city").all())
        if not districts:
            self.stdout.write(self.style.ERROR(
                "No districts found. Run: python manage.py seed_locations first."
            ))
            return

        amenities = list(Amenity.objects.all())

        sample_addresses = [
            "ul. Ivan Vazov 12",
            "bul. Vitosha 88",
            "ul. Shipka 4",
            "bul. Bulgaria 112",
            "ul. Oborishte 23",
            "ul. Slivnitsa 7",
            "bul. Cherni Vrah 51",
            "ul. Rakovski 99",
            "ul. Alabin 15",
            "ul. Graf Ignatiev 10",
        ]

        adjectives = ["Beautiful", "Sunny", "Cozy", "Spacious", "Modern", "Stylish", "Renovated", "Bright"]
        features = ["Garage", "Parking", "Near metro", "Panoramic view", "South exposure", "Quiet street", "New building"]
        purposes = ["for sale"]

        created = 0

        for i in range(12):  # create 12 sample listings (adjust)
            district = random.choice(districts)
            city_label = district.city.get_name_display() if hasattr(district.city, "get_name_display") else str(district.city)
            district_label = district.get_name_display() if hasattr(district, "get_name_display") else str(district)

            bedrooms = random.choice([1, 2, 3])
            rooms = max(bedrooms + 1, random.choice([2, 3, 4, 5]))
            size = random.choice([45, 60, 75, 90, 110, 140])
            price = random.choice([85000, 120000, 165000, 220000, 350000])

            # exposures
            exposure_count = random.choice([1, 2])
            exposure = random.sample([c[0] for c in AptExposureChoices.choices], k=exposure_count)

            # build a human-friendly name
            adjective = random.choice(adjectives)
            purpose = random.choice(purposes)
            extra = random.choice(features)

            listing_name = f"{adjective} {bedrooms}-bedroom apartment in {city_label} {district_label} {purpose} with {extra}"

            address = f"{sample_addresses[i % len(sample_addresses)]}, {city_label}"

            prop = Property.objects.create(
                name=listing_name,
                address=address,
                size=size,
                bedrooms=bedrooms,
                rooms=rooms,
                bathrooms=random.choice([1, 2]),
                balconies=random.choice([0, 1, 2]),
                price=price,
                district=district,
                property_type=random.choice([c[0] for c in PropertyTypeChoices.choices]),
                build_year=random.choice([1998, 2005, 2012, 2018, 2022]),
                build_type=random.choice([c[0] for c in BuildTypeChoices.choices]),
                description="Sample listing generated for testing views and UI.",
                heating=random.choice([c[0] for c in HeatingTypeChoices.choices]),
                exposure=exposure,
                floor=str(random.choice([1, 2, 3, 4, 5, 6, 7, 8])),
            )

            # Randomly attach 0–3 amenities if you have them seeded
            if amenities:
                chosen = random.sample(amenities, k=random.randint(0, min(3, len(amenities))))
                prop.amenities.set(chosen)

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {created} sample properties using seeded districts."
        ))