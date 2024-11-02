from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from routes.models import Country, City, Airport, Route
from routes.serializers import CountrySerializer, CitySerializer, AirportSerializer, RouteSerializer, \
    CityListSerializer, AirportlistSerializer, RouteListSerializer


class CountryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CityViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = City.objects.select_related("country")

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        return CitySerializer


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.select_related("closest_big_city")

    def get_serializer_class(self):
        if self.action == "list":
            return AirportlistSerializer
        return AirportSerializer


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = RouteSerializer
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer
