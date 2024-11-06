from django.urls import path, include
from rest_framework import routers

from airport.views import PositionViewSet, StaffViewSet, FlightViewSet, OrderViewSet

app_name = "airport"

router = routers.DefaultRouter()
router.register("positions", PositionViewSet)
router.register("staff", StaffViewSet)
router.register("flights", FlightViewSet)
router.register("order", OrderViewSet)


urlpatterns = [path("", include(router.urls))]
