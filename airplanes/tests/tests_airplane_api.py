from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airplanes.models import Airplane, AirplaneType, Manufacturer
from airplanes.serializers import (
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneTypeSerializer,
    ManufacturerSerializer,
)

AIRPLANE_URL = reverse("airplanes:airplane-list")
AIRPLANE_TYPE_URL = reverse("airplanes:airplanetype-list")
MANUFACTURER_URL = reverse("airplanes:manufacturer-list")


def update_url(url_name, instance_id):
    return reverse(f"airplanes:{url_name}-detail", args=(instance_id,))


def sample_airplane_type(**params) -> AirplaneType:
    defaults = {
        "name": "type1",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane_manufacturer(**params) -> Manufacturer:
    defaults = {
        "name": "manufacturer1",
    }
    defaults.update(params)
    return Manufacturer.objects.create(**defaults)


def sample_airplane(**params) -> Airplane:
    airplane_type = sample_airplane_type()
    manufacturer = sample_airplane_manufacturer()
    defaults = {
        "name": "airplane1",
        "rows": "10",
        "seats_in_row": "10",
        "airplane_type": airplane_type,
        "manufacturer": manufacturer,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airplane_list(self):
        sample_airplane()
        res = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_airplane_type_list(self):
        sample_airplane_type()
        res = self.client.get(AIRPLANE_TYPE_URL)
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_manufacturer_list(self):
        sample_airplane_manufacturer()
        res = self.client.get(MANUFACTURER_URL)
        manufacturer = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturer, many=True)
        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_airplane_type_forbidden(self):
        payload = {"name": "type1"}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_manufacturer_forbidden(self):
        payload = {"name": "type1"}
        res = self.client.post(MANUFACTURER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airplane_forbidden(self):
        airplane_type = sample_airplane_type()
        manufacturer = sample_airplane_manufacturer()
        payload = {
            "name": "airplane1",
            "rows": "10",
            "seats_in_row": "10",
            "airplane_type": airplane_type,
            "manufacturer": manufacturer,
        }

        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.test", password="adminpassword", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane_type(self):
        payload = {"name": "type1"}
        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_manufacturer(self):
        payload = {"name": "type1"}
        res = self.client.post(MANUFACTURER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_airplane(self):
        airplane_type = sample_airplane_type()
        manufacturer = sample_airplane_manufacturer()
        payload = {
            "name": "airplane1",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type.id,
            "manufacturer": manufacturer.id,
        }

        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airplane.objects.count(), 1)

    def test_update_airplane_type(self):
        airplane_type = sample_airplane_type()
        payload = {"name": "type2"}
        res = self.client.patch(update_url("airplanetype", airplane_type.id), payload)
        airplane_type = AirplaneType.objects.get(id=airplane_type.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], airplane_type.name)

    def test_update_manufacturer(self):
        manufacturer = sample_airplane_manufacturer()
        payload = {"name": "manufacturer2"}
        res = self.client.patch(update_url("manufacturer", manufacturer.id), payload)
        manufacturer = Manufacturer.objects.get(id=manufacturer.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], manufacturer.name)

    def test_update_airplane(self):
        airplane = sample_airplane()
        payload = {"name": "new_name"}
        res = self.client.patch(update_url("airplane", airplane.id), payload)
        airplane = Airplane.objects.get(id=airplane.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], airplane.name)
