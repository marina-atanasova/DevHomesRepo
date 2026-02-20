from django.shortcuts import render
from CreditCalculator.forms import CreditCalculator, calculator


# Create your views here.

def calculator_view(request):

    form = CreditCalculator(request.GET or None)
    context = {"form": form}

    print("GET:", request.GET)
    print("VALID:", form.is_valid(), "ERRORS:", form.errors)

    if request.GET and form.is_valid():
        property_price = form.cleaned_data.get("property_price")
        interest_rate_yearly = form.cleaned_data.get("interest_rate_yearly")
        self_funded_sum = form.cleaned_data.get("self_funded_sum")
        repayment_years = form.cleaned_data.get("repayment_years")

        monthly_payment = calculator(property_price, interest_rate_yearly, self_funded_sum, repayment_years)
        loan_amount = property_price - self_funded_sum
        context.update({
            "monthly_payment": monthly_payment,
            "loan_amount": loan_amount,
            "self_funded_sum": self_funded_sum,
        })

    return render(request, "CreditCalculator/calculator.html", context)