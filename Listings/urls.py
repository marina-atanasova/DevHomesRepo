from django.urls import path
from . import views
from .views import PropertyDetailView, AddListingView, AllListings, EditListingView

app_name = "listings"

urlpatterns = [
    path("", views.AllListings.as_view(), name="all"),
    path("search/", views.listings_search, name="search"),
    path("add/", AddListingView.as_view(), name="add"),
    path("<int:pk>/edit/", EditListingView.as_view(), name="edit"),
    path("<int:pk>/details", PropertyDetailView.as_view(), name="detail"),

]
