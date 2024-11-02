from rest_framework import serializers

from airplanes.models import Airplane, AirplaneType, Manufacturer


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "manufacturer",
            "image",
        )


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    manufacturer = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "manufacturer",
            "image",
        )


# class AirplaneImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Airplane
#         fields = ("id", "image",)
