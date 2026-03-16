from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render




urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),
    path("listings/", include("Listings.urls")),
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("", include("CreditCalculator.urls")),


]
