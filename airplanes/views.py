from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from airplanes.models import Airplane, Manufacturer, AirplaneType
from airplanes.serializers import (
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneTypeSerializer,
    ManufacturerSerializer,
)

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of airplanes",
    ),
    update=extend_schema(
        summary="Update one airplane (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update one airplane (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new airplane (Admin only)",
    ),
)
class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.select_related("airplane_type", "manufacturer")

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        return AirplaneSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of airplane types",
    ),
    update=extend_schema(
        summary="Update one airplane type (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update one airplane type (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new airplane type (Admin only)",
    ),
)
class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of manufacturers",
    ),
    update=extend_schema(
        summary="Update manufacturer (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update manufacturer (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new manufacturer (Admin only)",
    ),
)
class ManufacturerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
