from django.db import models


class MessageStatusChoices(models.TextChoices):
    NEW = "NEW", "New"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    CLOSED = "CLOSED", "Closed"

class RequestTypeChoices(models.TextChoices):
    BUY = "BUY", "Buy"
    SELL = "SELL", "Sell"
    OTHER = "OTHER", "Other"