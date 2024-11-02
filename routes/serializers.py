from rest_framework import serializers

from routes.models import Country, City, Airport, Route


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name", "country",)


class CityListSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = City
        fields = ("name", "country",)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name", "closest_big_city",)


class AirportlistSerializer(serializers.ModelSerializer):
    closest_big_city = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="city_country"
    )

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="airport_info"
    )
    destination = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="airport_info"
    )

    class Meta:
        model = Route
        fields = ("source", "destination", "distance")