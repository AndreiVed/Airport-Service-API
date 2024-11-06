from django.db.models import Count, F
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import Position, Staff, Flight, Order
from airport.serializers import (
    PositionSerializer,
    StaffSerializer,
    FlightListSerializer,
    FlightSerializer,
    FlightDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
    StaffListSerializer
)


class PositionViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()


class StaffViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = StaffSerializer
    queryset = Staff.objects.select_related("position")

    def get_serializer_class(self):
        if self.action == "list":
            return StaffListSerializer
        return StaffSerializer


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Flight.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related("airplane")
                .annotate(tickets_available=F("airplane__seats_in_row") * F("airplane__rows") - Count("tickets"))
            ).order_by("id")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related(
        "order__flight__airplane", "order__flight__route"
    )

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
