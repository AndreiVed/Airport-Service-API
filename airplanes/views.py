from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airplanes.models import Airplane, Manufacturer, AirplaneType
from airplanes.serializers import AirplaneSerializer


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = AirplaneSerializer
    queryset = Airplane.objects.select_related("airplane_type", "manufacturer")


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneSerializer


class ManufacturerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Manufacturer.objects.all()
    serializer_class = AirplaneSerializer
