from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from CreditCalculator.calculations import calculate_early_repayment_comparison
from CreditCalculator.forms import CreditCalculator, calculator, EarlyRepaymentCalculatorForm
from CreditCalculator.models import CreditRequest


# Create your views here.

def calculator_view(request):

    form = CreditCalculator(request.GET or None)
    context = {"form": form}


    if request.GET and form.is_valid():
        created_by = request.user if request.user.is_authenticated else None,
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
            created_by = request.user if request.user.is_authenticated else None

        )

        monthly_payment = calculator(property_price, interest_rate_yearly, self_funded_sum, repayment_years)
        loan_amount = property_price - self_funded_sum
        context.update({
            "monthly_payment": monthly_payment,
            "loan_amount": loan_amount,
            "self_funded_sum": self_funded_sum,
        })

    return render(request, "CreditCalculator/calculator.html", context)

def early_repayment_calculator_view(request):
    form = EarlyRepaymentCalculatorForm(request.GET or None)
    context = {"form": form}

    if request.GET and form.is_valid():
        try:
            results = calculate_early_repayment_comparison(
                principal=form.cleaned_data["current_principal"],
                yearly_interest_rate=form.cleaned_data["yearly_interest_rate"],
                monthly_payment=form.cleaned_data["monthly_payment"],
                early_monthly_payment=form.cleaned_data["early_monthly_payment"],
                life_insurance_monthly=form.cleaned_data.get("life_insurance_monthly"),
                property_insurance_yearly=form.cleaned_data.get("property_insurance_yearly"),
                bank_fee_rate_yearly=form.cleaned_data.get("bank_fee_rate_yearly"),
            )
            context.update(results)
        except ValueError as exc:
            form.add_error(None, str(exc))

    return render(request, "CreditCalculator/early_repayment_calculator.html", context)


class AllCreditRequests(generic.ListView):
    model = CreditRequest
    context_object_name = "credit_requests"
    template_name = "CreditCalculator/credit_all.html"

class DeleteCreditRequest(generic.DeleteView):
    model = CreditRequest
    template_name = "CreditCalculator/credit_delete.html"
    success_url = reverse_lazy("CreditCalculator:credit_all")