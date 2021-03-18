from django.shortcuts import render
from apis.models import Event, ParkingLot, ParkingSpot

def home(request):
    return render(request, 'web/signUp.html')

def reserve(request):
    events = Event.objects.order_by('-date')[:4]
    return render(request, 'web/reserveSpot.html', {'events': events})