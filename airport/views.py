from datetime import datetime

from django.db.models import Count, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, OpenApiResponse
from rest_framework import mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
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
    StaffListSerializer,
)

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of positions",

    ),
    update=extend_schema(
        summary="Update position (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update position (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new position (Admin only)",
    ),
)
class PositionViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of staff members",

    ),
    update=extend_schema(
        summary="Update one of staff members (Admin only)",

    ),
    partial_update=extend_schema(
        summary="Partial update one of staff member (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new staff member (Admin only)",
    ),
)
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


class OrderAndFlightPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100


@extend_schema_view(
    update=extend_schema(
        summary="Update flight (Admin only)",

    ),
    retrieve=extend_schema(
        summary="Retrieve one flight",
    ),

    partial_update=extend_schema(
        summary="Partial update flight (Admin only)",
    ),
    create=extend_schema(
        summary="Create a new flight (Admin only)",
    ),
)
class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Flight.objects.all()
    pagination_class = OrderAndFlightPagination

    @staticmethod
    def _params_to_int(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        routes = self.request.query_params.get("route")
        destination_city = self.request.query_params.get("destination_city")
        date = self.request.query_params.get("date")

        if routes:
            routes = self._params_to_int(routes)
            queryset = queryset.filter(route__id__in=routes)

        if destination_city:
            queryset = queryset.filter(
                route__destination__closest_big_city__name__icontains=destination_city
            )
        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_date__date=date)

        if self.action == "list":
            queryset = (
                queryset.select_related("airplane").annotate(
                    tickets_available=F("airplane__seats_in_row") * F("airplane__rows")
                    - Count("tickets")
                )
            ).order_by("id")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


    @extend_schema(
        summary="Retrieve all flights",
        parameters=[
            OpenApiParameter(
                "destination_city",
                type=OpenApiTypes.INT,
                description="Filter by destination city (ex. ?destination_city=kyiv)",
            ),
            OpenApiParameter(
                "route",
                type=OpenApiTypes.INT,
                description="Filter by route (ex. ?route=1,2)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description=(
                    "Filter by departure date "
                    "(ex. ?date=2022-11-19)"
                ),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve list of your orders",
    ),
    retrieve=extend_schema(
        summary="Retrieve one of your orders",
    ),
    create=extend_schema(
        summary="Create a new order",
    ),
)
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
    permission_classes = (IsAuthenticated,)
    pagination_class = OrderAndFlightPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
