from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    eventId = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class ParkingSpot(models.Model):
    spotType = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    eventsReserved = 

class ParkingLot(models.Model):
    spots
    eventsAvailable
    attendants

    def getAvailableSpots()

    def addParkingSpot()

class Reservation(model.Model):
    parkingSpot
    event
    ticket = models.IntegerField(default=0)

class Permission(model.Model):
    name = models.CharField(max_length=200)

class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    permissions = 
    reservations
    accountBalance = models.FloatField(default=100.0)

    def reserve(parkingSpot, event)

    def useReservation(reservation)

class Attendant(models.Model):
    parkingLot = models.ForeignKey(ParkingLot)

    def checkIn()

class Owner(models.Model):
    parkingLots

    def assignAttendant(username, parkingLot)

    def registerLot(parkingLot)

    def addParkingSpot(parkingLot, parkingSpot)

    def openLot(parkingLot, event)

class Admin(models.Model):

    def createOwner(username)

    def addEvent(event)