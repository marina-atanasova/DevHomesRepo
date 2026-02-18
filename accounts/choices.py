from django.db import models


class MessageStatusChoices(models.TextChoices):
    NEW = "NEW", "New"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    CLOSED = "CLOSED", "Closed"