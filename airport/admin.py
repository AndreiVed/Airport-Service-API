from django.contrib import admin

from airport.models import Position, Staff, Flight, Order, Ticket

admin.site.register(Position)
admin.site.register(Staff)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
