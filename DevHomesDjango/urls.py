from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home_view(request):
    return render(request, "home.html")

def contact_view(request):
    return render(request, "contact.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home_view, name="home"),
    path("contact/", contact_view, name="contact"),

    path("listings/", include("Listings.urls")),
]
