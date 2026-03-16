from django.urls import path
from . import views
from .views import PropertyDetailView, AddListingView, AllListings, EditListingView, DeleteListingView, AmenityListView, \
    AmenityCreateView, AmenityDetailView, AmenityUpdateView, AmenityDeleteView

app_name = "listings"

urlpatterns = [
    path("", views.AllListings.as_view(), name="all"),
    path("search/", views.listings_search, name="search"),
    path("add/", AddListingView.as_view(), name="add"),
    path("<int:pk>/edit/", EditListingView.as_view(), name="edit"),
    path("<int:pk>/details", PropertyDetailView.as_view(), name="detail"),
    path("<int:pk>/delete", DeleteListingView.as_view(), name="delete"),
    path("amenities/", AmenityListView.as_view(), name="all_amenities"),
    path("amenities/add/", AmenityCreateView.as_view(), name="add_amenity"),
    path("amenities/<int:pk>/", AmenityDetailView.as_view(), name="amenity_detail"),
    path("amenities/<int:pk>/edit/", AmenityUpdateView.as_view(), name="edit_amenity"),
    path("amenities/<int:pk>/delete/", AmenityDeleteView.as_view(), name="delete_amenity"),


]
