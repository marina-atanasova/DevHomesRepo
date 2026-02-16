from django.urls import path
from . import views
from .views import PropertyDetailView, AddListingView

app_name = "listings"

urlpatterns = [
    path("", views.listings_all, name="all"),         # /listings/
    path("search/", views.listings_search, name="search"),
    path("add/", AddListingView.as_view(), name="add"),

    path("<int:pk>/", PropertyDetailView.as_view(), name="detail"),
]
