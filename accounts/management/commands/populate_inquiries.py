import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import UserInquiry
from accounts.choices import MessageStatusChoices, RequestTypeChoices
from Listings.models import Property


class Command(BaseCommand):
    help = "Populate the database with sample contact inquiries."

    @transaction.atomic
    def handle(self, *args, **options):
        UserInquiry.objects.all().delete()

        properties = list(Property.objects.all())
        if not properties:
            self.stdout.write(
                self.style.ERROR(
                    "No properties found. Run `python manage.py populate_db` first."
                )
            )
            return

        first_names = ["Ivan", "Maria", "Georgi", "Elena", "Petar", "Nikolay"]
        last_names = ["Ivanov", "Petrova", "Dimitrov", "Georgieva", "Kolev", "Todorova"]
        messages = [
            "I am interested in this property. Is it still available?",
            "Can we schedule a viewing this week?",
            "Is the price negotiable?",
            "Please send more photos and details.",
            "I would like to discuss financing options.",
        ]
        statuses = [
            MessageStatusChoices.NEW,
            MessageStatusChoices.IN_PROGRESS,
            MessageStatusChoices.CLOSED,
        ]

        created = 0

        for i in range(10):
            first = random.choice(first_names)
            last = random.choice(last_names)
            status = random.choice(statuses)
            created_time = timezone.now() - timedelta(days=random.randint(0, 10))

            inquiry = UserInquiry.objects.create(
                first_name=first,
                last_name=last,
                phone=f"08{random.randint(10000000, 99999999)}",
                email=f"{first.lower()}.{last.lower()}{i}@example.com",
                listing=random.choice(properties),
                request_type=random.choice([c[0] for c in RequestTypeChoices.choices]),
                message=random.choice(messages),
                status=status,
            )

            inquiry.created_at = created_time

            if status == MessageStatusChoices.IN_PROGRESS:
                inquiry.reply_message = "Thank you for your interest. We will contact you shortly."
                inquiry.replied_at = created_time + timedelta(hours=2)

            if status == MessageStatusChoices.CLOSED:
                inquiry.reply_message = "This property is no longer available. We can suggest alternatives."
                inquiry.replied_at = created_time + timedelta(hours=1)
                inquiry.closed_at = created_time + timedelta(days=1)

            inquiry.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} sample inquiries."))
