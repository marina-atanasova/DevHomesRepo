from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def dashboard(request):
    user = request.user

    context = {
        "user": user,
        "favorite_listings": user.favorite_properties.all(),
        "inquiries": user.inquiries.all(),
        "credit_requests": user.credit_requests.all(),
        "my_listings": user.broker_listings.all() if user.role == "broker" else [],

    }

    return render(request, "users/dashboard.html", context)
