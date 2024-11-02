from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from routes.views import CountryViewSet, CityViewSet, AirportViewSet, RouteViewSet

app_name = "routes"

router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]
