import random
from django.core.management.base import BaseCommand
from Listings.models import City, District, Property
from Listings.choices import CityChoices, DistrictChoices, PropertyTypeChoices, BuildTypeChoices, HeatingTypeChoices, AptExposureChoices

class Command(BaseCommand):
    help = "Populate database with sample cities, districts and properties."

    def handle(self, *args, **options):
        # Cities
        city_objs = {}
        for value, _label in CityChoices.choices:
            city, _ = City.objects.get_or_create(name=value)
            city_objs[value] = city

        # Districts: create a subset for each city (including repeats like Center)
        districts_by_city = {}
        for city in city_objs.values():
            districts = []
            for d_value, _ in DistrictChoices.choices:
                district, _ = District.objects.get_or_create(city=city, name=d_value)
                districts.append(district)
            districts_by_city[city.name] = districts

        # Properties
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

        created = 0
        for i in range(10):
            city_name = random.choice(list(city_objs.keys()))
            district = random.choice(districts_by_city[city_name])

            address = f"{sample_addresses[i % len(sample_addresses)]}, {city_name}"
            exposure_count = random.choice([1, 2])
            exposure = random.sample([c[0] for c in AptExposureChoices.choices], k=exposure_count)

            Property.objects.create(
                address=address,
                size=random.choice([45, 60, 75, 90, 110, 140]),
                bedrooms=random.choice([1, 2, 3]),
                rooms=random.choice([2, 3, 4]),
                bathrooms=random.choice([1, 2]),
                balconies=random.choice([0, 1, 2]),
                price=random.choice([85000, 120000, 165000, 220000, 350000]),
                district=district,
                property_type=random.choice([c[0] for c in PropertyTypeChoices.choices]),
                build_year=random.choice([1998, 2005, 2012, 2018, 2022]),
                build_type=random.choice([c[0] for c in BuildTypeChoices.choices]),
                description="Sample listing generated for testing views.",
                heating=random.choice([c[0] for c in HeatingTypeChoices.choices]),
                exposure=exposure,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Populated DB with cities, districts and {created} properties."))
