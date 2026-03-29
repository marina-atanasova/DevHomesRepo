from rest_framework import serializers
from Listings.models import Amenity, Property

EXPOSURE_LABELS = {
    "N": "North",
    "S": "South",
    "E": "East",
    "W": "West",
}
VALID_EXPOSURES = set(EXPOSURE_LABELS.keys())


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class ListingSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Amenity.objects.all(),
        write_only=True,
        source="amenities",
        required=False,
    )
    price_per_sqm = serializers.ReadOnlyField()
    exposure_input = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "address",
            "city",
            "district",
            "size",
            "price",
            "bedrooms",
            "rooms",
            "bathrooms",
            "balconies",
            "property_type",
            "build_year",
            "build_type",
            "description",
            "heating",
            "floor",
            "broker",
            "amenities",
            "amenity_ids",
            "price_per_sqm",
            "exposure",
            "exposure_input",
        ]
        read_only_fields = [
            "id",
            "broker",
            "price_per_sqm",

        ]


    def validate_exposure_input(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Exposure cannot be empty.")

        parts = [item.strip().upper() for item in value.split(",") if item.strip()]

        if not parts:
            raise serializers.ValidationError("Exposure cannot be empty.")

        invalid = [item for item in parts if item not in VALID_EXPOSURES]
        if invalid:
            raise serializers.ValidationError(
                f"Invalid exposure values: {', '.join(invalid)}. "
                f"Allowed values are: {', '.join(sorted(VALID_EXPOSURES))}."
            )

        return parts

    def validate(self, attrs):
        request = self.context.get("request")
        method = request.method if request else None

        # On create, require either exposure_input or exposure
        if method == "POST":
            if not attrs.get("exposure") and not attrs.get("exposure_input"):
                raise serializers.ValidationError({
                    "exposure": "Provide exposure or exposure_input."
                })

        return attrs
    def create(self, validated_data):
        exposure_input = validated_data.pop("exposure_input")
        validated_data["exposure"] = exposure_input
        return super().create(validated_data)

    def update(self, instance, validated_data):
        exposure_input = validated_data.pop("exposure_input", None)
        if exposure_input is not None:
            validated_data["exposure"] = exposure_input
        return super().update(instance, validated_data)