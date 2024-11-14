from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from routes.models import Country, City, Airport, Route
from routes.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    CityListSerializer,
    AirportlistSerializer,
    RouteListSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of countries",
    ),
    update=extend_schema(
        summary="Update country (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update country (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new country (Admin only)",
    ),
)
class CountryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of cities",
    ),
    update=extend_schema(
        summary="Update city (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update city (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new city (Admin only)",
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of airports",
    ),
    update=extend_schema(
        summary="Update airport (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update airport (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new airport (Admin only)",
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of routes",
    ),
    update=extend_schema(
        summary="Update route (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update route (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new route (Admin only)",
    ),
)
class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer
