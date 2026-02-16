from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.views.generic import DetailView, CreateView

from .models import Property

def listings_all(request):
    listings = Property.objects.all().order_by("-id")
    return render(request, "Listings/all_listings.html", {"listings": listings})

def listings_search(request):
    # placeholder for now
    return render(request, "Listings/search.html")

class PropertyDetailView(DetailView):
    model = Property
    template_name = "Listings/property_detail.html"

class AddListingView(CreateView):
    model = Property
    fields = "__all__"
    template_name = "Listings/add_listing.html"
    success_url = "/listings/:all"


def listings_add(request):
    # placeholder for now
    return render(request, "Listings/add_listing.html")
