from django.contrib import admin

from .models import CreditRequest


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'linked_property', 'property_price')