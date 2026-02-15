from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Property

def listings_all(request):
    listings = Property.objects.all().order_by("-id")
    return render(request, "Listings/all_listings.html", {"listings": listings})

def listings_search(request):
    # placeholder for now
    return render(request, "Listings/search.html")

def listings_add(request):
    # placeholder for now
    return render(request, "Listings/add_listing.html")
