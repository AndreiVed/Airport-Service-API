from django.db import models
from django.db.models import CASCADE


class Country(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=63, unique=True)
    country = models.ForeignKey(Country, on_delete=CASCADE, related_name="cities")

    @property
    def city_country(self) -> str:
        return f"{self.name} - {self.country}"

    def __str__(self):
        return f"{self.name} - {self.country}"


class Airport(models.Model):
    name = models.CharField(max_length=63, unique=True)
    closest_big_city = models.ForeignKey(
        City,
        on_delete=CASCADE,
        related_name="airports",
    )

    @property
    def airport_info(self) -> str:
        return (
            f"{self.name} - "
            f"{self.closest_big_city.name} "
            f"({self.closest_big_city.country})"
        )

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.closest_big_city.name} "
            f"({self.closest_big_city.country})"
        )


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=CASCADE,
        related_name="sources",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=CASCADE,
        related_name="destinations",
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}"

    @property
    def route_info(self):
        return f"{self.source} -> {self.destination}"

    class Meta:
        ordering = ["source"]
