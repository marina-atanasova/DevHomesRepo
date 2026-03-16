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
