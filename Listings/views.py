from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.

from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from .forms import PropertyForm
from django.shortcuts import render
from .models import Property
from .forms import ListingsSearchForm


class AllListings(ListView):
    model = Property
    paginate_by = 6

    context_object_name = "listings"
    template_name = "Listings/all_listings.html"

    def get_queryset(self):
        return Property.objects.all().order_by("-id")


def listings_search(request):
    form = ListingsSearchForm(request.GET or None)
    qs = Property.objects.all().order_by("-id")



    if request.GET and form.is_valid():
        q = form.cleaned_data.get("q")
        district = form.cleaned_data.get("district")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        rooms = form.cleaned_data.get("rooms")
        amenities = form.cleaned_data.get("amenities")
        city = form.cleaned_data.get("city")

        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(address__icontains=q)
                | Q(district__name__icontains=q)
                | Q(district__city__name__icontains=q)
            )
        if district:
            qs = qs.filter(district=district)
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        if rooms is not None:
            qs = qs.filter(rooms__gte=rooms)
        if amenities:
            qs = qs.filter(amenities__in=amenities).distinct()
        if city:
            qs = qs.filter(district__city=city)

    return render(request, "Listings/search.html", {"form": form, "listings": qs})


class PropertyDetailView(DetailView):
    model = Property
    template_name = "Listings/property_detail.html"

class AddListingView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = "Listings/add_listing.html"
    success_url = "/listings"


class EditListingView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = "Listings/edit_listing.html"
    success_url = "/listings"

class DeleteListingView(DeleteView):
    model = Property
    success_url = "/listings"
    template_name = "Listings/delete_listing.html"