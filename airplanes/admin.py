from django.contrib import admin

from airplanes.models import AirplaneType, Airplane, Manufacturer

admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Manufacturer)
