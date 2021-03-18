from django.shortcuts import render
from apis.models import Event, ParkingLot, ParkingSpot

def home(request):
    return render(request, 'web/signUp.html')

def reserve(request):
    events = Event.objects.order_by('-date')[:4]
    return render(request, 'web/reserveSpot.html', {'events': events})

def login(request):
    return render(request, 'web/login.html')

def main(request):
    return render(request, 'web/main.html')

def account(request):
    return render(request, 'web/account.html')

def history(request):
    return render(request, 'web/pastReservations.html')

def attendant(request):
    return render(request, 'web/attendant.html')