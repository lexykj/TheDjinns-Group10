from django.contrib import admin

from .models import Event, ParkingLot, ParkingSpot, User, Reservation

admin.site.register((Event, ParkingLot, ParkingSpot, User, Reservation))
