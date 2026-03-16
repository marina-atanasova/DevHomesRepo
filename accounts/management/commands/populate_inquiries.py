import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import UserInquiry
from accounts.choices import MessageStatusChoices, RequestTypeChoices
from Listings.models import Property


class Command(BaseCommand):
    help = "Populate DB with sample contact inquiries."

    @transaction.atomic
    def handle(self, *args, **options):
        # Optional: clear existing inquiries
        UserInquiry.objects.all().delete()

        properties = list(Property.objects.all())

        if not properties:
            self.stdout.write(self.style.WARNING(
                "⚠ No properties found. Inquiries will be created without linked listings."
            ))

        first_names = ["Ivan", "Maria", "Georgi", "Elena", "Petar", "Nikolay", "Desislava", "Stoyan"]
        last_names = ["Ivanov", "Petrova", "Dimitrov", "Georgieva", "Kolev", "Todorova"]
        messages = [
            "I am interested in this property. Is it still available?",
            "Can we schedule a viewing this week?",
            "Is the price negotiable?",
            "Please send more photos and details.",
            "I would like to discuss financing options.",
            "Is there parking included?",
            "How old is the building?",
            "Are pets allowed in this building?",
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
                phone=f"+35988{random.randint(1000000, 9999999)}",
                email=f"{first.lower()}.{last.lower()}{i}@example.com",
                listing=random.choice(properties) if properties else None,
                request_type=random.choice([c[0] for c in RequestTypeChoices.choices]),
                message=random.choice(messages),
                status=status,
            )

            # Manually adjust timestamps after creation
            inquiry.created_at = created_time

            if status == MessageStatusChoices.IN_PROGRESS:
                inquiry.reply_message = "Thank you for your interest. We will contact you shortly."
                inquiry.replied_at = created_time + timedelta(hours=2)

            if status == MessageStatusChoices.CLOSED:
                inquiry.reply_message = "The property has been sold. Let us know if you need alternatives."
                inquiry.replied_at = created_time + timedelta(hours=1)
                inquiry.closed_at = created_time + timedelta(days=1)

            inquiry.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {created} sample inquiries with mixed statuses."
        ))