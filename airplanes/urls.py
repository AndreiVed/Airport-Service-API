from django.urls import path, include
from rest_framework import routers

from airplanes.views import AirplaneViewSet, AirplaneTypeViewSet, ManufacturerViewSet

app_name = "airplanes"

router = routers.DefaultRouter()
router.register("all", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("manufacturer", ManufacturerViewSet)


urlpatterns = [path("", include(router.urls))]
