from django.contrib import admin
from .models import Property, Amenity

# Register your models here.


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'district', 'price', 'broker')
    list_filter = ('city', 'district', 'property_type')
    search_fields = ('name', 'address')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)