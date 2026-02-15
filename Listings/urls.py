from django.urls import path
from . import views

app_name = "listings"

urlpatterns = [
    path("", views.listings_all, name="all"),         # /listings/
    path("search/", views.listings_search, name="search"),
    path("add/", views.listings_add, name="add"),
]
