from django import forms
from .models import District, Amenity, Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"
        widgets = {
            "amenities": forms.CheckboxSelectMultiple(),
        }


class ListingsSearchForm(forms.Form):
    district = forms.ModelChoiceField(
        queryset=District.objects.none(),
        required=False,
        empty_label="Any district",
        label="District",
    )

    min_price = forms.IntegerField(
        required=False,
        min_value=0,
        label="Min price",
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 80000"}),
    )

    max_price = forms.IntegerField(
        required=False,
        min_value=0,
        label="Max price",
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 200000"}),
    )

    rooms = forms.IntegerField(
        required=False,
        min_value=0,
        label="Rooms",
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 3"}),
    )

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Amenities",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["district"].queryset = District.objects.all().order_by("city__name", "name")
        self.fields["amenities"].queryset = Amenity.objects.all().order_by("name")

    def clean(self):
        cleaned = super().clean()
        min_price = cleaned.get("min_price")
        max_price = cleaned.get("max_price")

        if min_price is not None and max_price is not None and min_price > max_price:
            self.add_error("max_price", "Max price must be greater than or equal to Min price.")

        return cleaned
