from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login
from apis.models import Event, ParkingLot, ParkingSpot

def home(request):
    return render(request, 'web/signUp.html')

def reserve(request):
    events = Event.objects.order_by('-date')[:4]
    return render(request, 'web/reserveSpot.html', {'events': events})

def loginpage(request):
    return render(request, 'web/login.html')

def signIn(request):
    if request.user.is_authenicated:
        return redirect('/home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return render(request, 'web/login.html')
    else:
        return render(request, 'web/login.html')

def main(request):
    return render(request, 'web/main.html')

def account(request):
    return render(request, 'web/account.html')

def history(request):
    return render(request, 'web/pastReservations.html')

def attendant(request):
    return render(request, 'web/attendant.html')

def events(request):
    return render(request, 'web/eventManagement.html')

def owners(request):
    return render(request, 'web/ownerManagement.html')

def lots(request):
    return render(request, 'web/lotManagement.html')

def info(request):
    return render(request, 'web/lotInfo.html')