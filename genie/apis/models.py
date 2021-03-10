from django.db import models
from django.db.models.deletion import CASCADE

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('event date')

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    accountBalance = models.FloatField(default=100.0)

class Owner(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)

class ParkingLot(models.Model):
    event = models.ForeignKey(Event, on_delete=CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

class ParkingSpot(models.Model):
    spotType = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)

class Attendant(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)

class Reservation(models.Model):
    parkingSpot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.IntegerField(default=0)

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userPermish = models.BooleanField()
    attendantPermish = models.BooleanField()
    ownerPermish = models.BooleanField()
    adminPermish = models.BooleanField()

class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)