from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import Amenity


class Command(BaseCommand):
    help = "Seed common real estate amenities."

    @transaction.atomic
    def handle(self, *args, **options):
        amenities_list = [
            "Garage",
            "Parking",
            "Elevator",
            "Security",
            "Furnished",
            "Air Conditioning",
            "Central Heating",
            "Balcony",
            "Basement",
            "Storage Room",
            "Garden",
            "Swimming Pool",
            "Near Metro",
            "Sea View",
            "Mountain View",
        ]

        created = 0

        for name in amenities_list:
            obj, was_created = Amenity.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"✅ Seeded {created} amenities successfully.")
        )