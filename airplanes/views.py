from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from airplanes.models import Airplane, Manufacturer, AirplaneType
from airplanes.serializers import (
    AirplaneSerializer,
    AirplaneListSerializer,
    # AirplaneImageSerializer,
    AirplaneTypeSerializer,
    ManufacturerSerializer,
)


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    # serializer_class = AirplaneSerializer
    queryset = Airplane.objects.select_related("airplane_type", "manufacturer")

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        # if self.action == "upload_image":
        #     return AirplaneImageSerializer

        return AirplaneSerializer

    # @action(
    #     methods=["POST"],
    #     detail=True,
    #     url_path="upload-image",
    #     # permission_classes=[IsAdminUser],
    # )
    # def upload_image(self, request, pk=None):
    #     """Endpoint for uploading image to specific movie"""
    #     movie = self.get_object()
    #     serializer = self.get_serializer(movie, data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class ManufacturerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
