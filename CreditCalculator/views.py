from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from CreditCalculator.forms import CreditCalculator, calculator
from CreditCalculator.models import CreditRequest


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
        linked_property = form.cleaned_data.get("linked_property")


        CreditRequest.objects.create(
            property_price=property_price,
            interest_rate=interest_rate_yearly,
            down_payment=self_funded_sum,
            repayment_years=repayment_years,
            linked_property=linked_property,
        )

        monthly_payment = calculator(property_price, interest_rate_yearly, self_funded_sum, repayment_years)
        loan_amount = property_price - self_funded_sum
        context.update({
            "monthly_payment": monthly_payment,
            "loan_amount": loan_amount,
            "self_funded_sum": self_funded_sum,
        })

    return render(request, "CreditCalculator/calculator.html", context)

class AllCreditRequests(generic.ListView):
    model = CreditRequest
    context_object_name = "credit_requests"
    template_name = "CreditCalculator/credit_all.html"

class DeleteCreditRequest(generic.DeleteView):
    model = CreditRequest
    template_name = "CreditCalculator/credit_delete.html"
    success_url = reverse_lazy("CreditCalculator:credit_all")