from django.contrib import admin

from .models import Event, ParkingLot, ParkingSpot, Profile, Reservation

admin.site.register((Event, ParkingLot, ParkingSpot, Profile, Reservation))
