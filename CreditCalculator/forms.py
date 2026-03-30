from decimal import Decimal

from django import forms
from Listings.models import Property


def calculator(property_price: float, interest_rate_yearly: float, self_funded_sum: float, repayment_years: int):
    loan_amount = property_price - self_funded_sum
    repayment_months = repayment_years * 12
    interest_rate_monthly = interest_rate_yearly / 100 / 12

    if interest_rate_monthly == 0:
        return loan_amount / repayment_months

    monthly_payment = (loan_amount * (
            interest_rate_monthly * (1 + interest_rate_monthly) ** repayment_months) /
                       ((1 + interest_rate_monthly) ** repayment_months - 1))

    return monthly_payment

class CreditCalculator(forms.Form):
    linked_property = forms.ModelChoiceField(
        queryset=Property.objects.all(),
        required=False,
        empty_label="Select property (optional)",
        label="Linked Property"
    )

    property_price = forms.DecimalField(
        label="Property Price",
        widget=forms.NumberInput(attrs={'placeholder': 155000}),
        min_value=0
    )
    interest_rate_yearly = forms.DecimalField(
        label="Yearly Interest Rate",
        widget=forms.NumberInput(attrs={'placeholder': 2.5}),
        min_value=0
    )
    self_funded_sum = forms.DecimalField(
        label="Down Payment",
        widget=forms.NumberInput(attrs={'placeholder': 25000}),
        min_value=0
    )
    repayment_years = forms.IntegerField(
        label="Repayment Years",
        widget=forms.NumberInput(attrs={'placeholder':25}),
        min_value=1
    )

    def clean(self):
        cleaned = super().clean()
        self_funded_sum = cleaned.get("self_funded_sum")
        property_price = cleaned.get("property_price")

        if self_funded_sum is not None and property_price is not None and self_funded_sum > property_price:
            self.add_error("self_funded_sum", "Property price must be greater than or equal to your Down payment.")

        return cleaned


class EarlyRepaymentCalculatorForm(forms.Form):
    current_principal = forms.DecimalField(
        label="Current Remaining Principal",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "80000"})
    )
    yearly_interest_rate = forms.DecimalField(
        label="Yearly Interest Rate (%)",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "2.4"})
    )
    years_left = forms.IntegerField(
        label="Years Left",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "15"})
    )
    life_insurance_monthly = forms.DecimalField(
        label="Life Insurance Monthly (optional)",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "leave blank to estimate"})
    )
    property_insurance_yearly = forms.DecimalField(
        label="Property Insurance Per Year (optional)",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "leave blank to estimate"})
    )
    bank_fee_rate_yearly = forms.DecimalField(
        label="Bank Servicing Fee Yearly (% of remaining principal, optional)",
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": "leave blank to estimate"})
    )
    monthly_payment = forms.DecimalField(
        label="Current Monthly Payment",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "500"})
    )
    early_monthly_payment = forms.DecimalField(
        label="New Monthly Payment",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "800"})
    )

    def clean(self):
        cleaned = super().clean()

        current_principal = cleaned.get("current_principal")
        yearly_interest_rate = cleaned.get("yearly_interest_rate")
        monthly_payment = cleaned.get("monthly_payment")
        early_monthly_payment = cleaned.get("early_monthly_payment")

        if monthly_payment is not None and early_monthly_payment is not None:
            if early_monthly_payment <= monthly_payment:
                self.add_error(
                    "early_monthly_payment",
                    "New monthly payment must be higher than the current monthly payment."
                )

        if current_principal is not None and yearly_interest_rate is not None and monthly_payment is not None:
            monthly_rate = (yearly_interest_rate / Decimal("100")) / Decimal("12")
            monthly_interest_only = current_principal * monthly_rate

            if monthly_payment <= monthly_interest_only:
                self.add_error(
                    "monthly_payment",
                    "Current monthly payment is too low to reduce the principal."
                )

            if early_monthly_payment is not None and early_monthly_payment <= monthly_interest_only:
                self.add_error(
                    "early_monthly_payment",
                    "New monthly payment is too low to reduce the principal."
                )

        return cleaned