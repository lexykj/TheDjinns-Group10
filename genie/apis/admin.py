from django.contrib import admin

from .models import Event, ParkingLot, ParkingSpot, Profile, Reservation, Revenue

admin.site.register((Event, ParkingLot, ParkingSpot, Profile, Reservation, Revenue))
