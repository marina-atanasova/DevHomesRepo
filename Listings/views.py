from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, FormView, ListView, UpdateView

from .models import Property

class AllListings(ListView):
    model = Property
    paginate_by = 6

    context_object_name = "listings"
    template_name = "Listings/all_listings.html"

    def get_queryset(self):
        return Property.objects.all().order_by("-id")
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
    success_url = "/listings"


class EditListingView(UpdateView):
    model = Property
    fields = "__all__"
    template_name = "Listings/edit_listing.html"
    success_url = "/listings"

