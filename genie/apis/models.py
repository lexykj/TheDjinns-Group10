from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import uuid

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500, default='')
    date = models.DateTimeField('event date')
    address = models.CharField(max_length=500, blank=True, default='')
    latitude = models.FloatField(default=41.7429795162564)
    longitude = models.FloatField(default=111.809492111206)

    def __str__(self) -> str:
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.FloatField(default=100.0)

    is_customer = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    is_attendant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    attendant_for = models.ManyToManyField('ParkingLot', blank=True) # must check if is attendant

    def __str__(self) -> str:
        return self.user.username

class ParkingLot(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True, default='')
    latitude = models.FloatField(default=41.7429795162564)
    longitude = models.FloatField(default=111.809492111206)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # must check if user is_owner

    def __str__(self) -> str:
        return self.name

class ParkingSpot(models.Model):
    spotType = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    spots = models.IntegerField(default=1)

    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.spotType

class Reservation(models.Model):
    uuid = models.IntegerField(default=0)
    
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE) # no more spots than ParkingSpot.spot
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.uuid)

# admin.site.unregister(User)
# admin.site.register(User)