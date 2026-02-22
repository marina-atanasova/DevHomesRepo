from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import City, District, Property
from Listings.choices import CityChoices, DistrictChoices


class Command(BaseCommand):
    help = "Seed Cities and Districts with demo data."

    @transaction.atomic
    def handle(self, *args, **options):
        # Clear in correct order (district is PROTECTed by Property)
        Property.objects.all().delete()
        District.objects.all().delete()
        City.objects.all().delete()

        # Create cities
        cities = [
            CityChoices.SOFIA,
            CityChoices.PLOVDIV,
            CityChoices.VARNA,
            CityChoices.BURGAS,
            CityChoices.RUSE,
            CityChoices.SHUMEN,
            CityChoices.VIDIN,
        ]

        city_objs = {}
        for c in cities:
            city_obj = City.objects.create(name=c)
            city_objs[c] = city_obj

        # Sofia: 5 districts (as requested)
        sofia_districts = [
            DistrictChoices.CENTER,
            DistrictChoices.MLADOST,
            DistrictChoices.DRUJBA,
            DistrictChoices.VITOSHA,
            DistrictChoices.BOROVO,
        ]

        # Other cities: Center + 2-3 "unique" from your available set
        per_city_districts = {
            CityChoices.PLOVDIV: [DistrictChoices.CENTER, DistrictChoices.HIPODRUMA, DistrictChoices.NADEJA],
            CityChoices.VARNA: [DistrictChoices.CENTER, DistrictChoices.LIULIN, DistrictChoices.DRUJBA],
            CityChoices.BURGAS: [DistrictChoices.CENTER, DistrictChoices.VITOSHA, DistrictChoices.BOROVO],
            CityChoices.RUSE: [DistrictChoices.CENTER, DistrictChoices.MLADOST, DistrictChoices.NADEJA],
            CityChoices.SHUMEN: [DistrictChoices.CENTER, DistrictChoices.HIPODRUMA, DistrictChoices.DRUJBA],
            CityChoices.VIDIN: [DistrictChoices.CENTER, DistrictChoices.LIULIN, DistrictChoices.BOROVO],
        }

        # Create districts for Sofia
        for d in sofia_districts:
            District.objects.get_or_create(city=city_objs[CityChoices.SOFIA], name=d)

        # Create districts for other cities
        for city_choice, districts in per_city_districts.items():
            city_obj = city_objs[city_choice]
            for d in dict.fromkeys(districts):  # dedupe while preserving order
                District.objects.get_or_create(city=city_obj, name=d)

        self.stdout.write(self.style.SUCCESS("✅ Seeded Cities and Districts successfully."))