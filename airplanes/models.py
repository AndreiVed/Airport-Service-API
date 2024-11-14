import os
import uuid

from django.db import models
from django.db.models import CASCADE
from django.utils.text import slugify


def airplane_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplane/", filename)


class AirplaneType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=63, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=airplane_image_file_path)

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name
