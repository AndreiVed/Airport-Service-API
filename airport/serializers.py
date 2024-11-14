from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airplanes.serializers import AirplaneToFlightSerializer
from airport.models import Position, Staff, Flight, Ticket, Order
from routes.serializers import RouteListSerializer


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ("name",)


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ("first_name", "last_name", "position")


class StaffListSerializer(serializers.ModelSerializer):
    position = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Staff
        fields = ("first_name", "last_name", "position")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "staff",
            "departure_date",
            "arrival_time",
        )

    def validate(self, attrs):
        data = super(FlightSerializer, self).validate(attrs=attrs)
        Flight.validate_departure_and_arrival_dates(
            attrs["departure_date"], attrs["arrival_time"], ValidationError
        )
        return data


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="route_info"
    )
    airplane = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    staff = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    departure_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "staff",
            "departure_date",
            "arrival_time",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    route = RouteListSerializer(many=False, read_only=True)

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"], attrs["seat"], attrs["flight"].airplane, ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "route")


class TicketListSerializer(TicketSerializer):
    route = RouteListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightListSerializer):
    route = RouteListSerializer()
    airplane = AirplaneToFlightSerializer()
    taken_places = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "staff",
            "departure_date",
            "arrival_time",
            "taken_places",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ("id", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")
