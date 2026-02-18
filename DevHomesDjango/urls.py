from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home_view, name="home"),

    path("listings/", include("Listings.urls")),
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),


]
