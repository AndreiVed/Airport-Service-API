from django.utils import timezone
from django.db import models
from django.db.models import CASCADE
from rest_framework.exceptions import ValidationError

from airplanes.models import Airplane
from airport_service import settings
from routes.models import Route


class Position(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    position = models.ForeignKey(Position, on_delete=CASCADE)

    class Meta:
        unique_together = ("first_name", "last_name", "position")
        ordering = ["position"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} - {self.position}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=CASCADE)
    staff = models.ManyToManyField(Staff, related_name="flights")
    departure_date = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["route"]

    def __str__(self):
        return str(self.route)

    @staticmethod
    def validate_departure_and_arrival_dates(
        departure_date, arrival_time, error_to_raise
    ):
        if departure_date > arrival_time:
            raise error_to_raise(
                f"'Departure date' must be earlier than 'arrival time'"
            )
        if departure_date < timezone.now() or arrival_time < timezone.now():
            raise error_to_raise(
                f"'Departure date' and 'arrival time' "
                f"must be not earlier than time now"
            )

    def clear(self):
        Flight.validate_departure_and_arrival_dates(
            departure_date=self.departure_date,
            arrival_time=self.arrival_time,
            error_to_raise=ValidationError,
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.id}," f"created: {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
