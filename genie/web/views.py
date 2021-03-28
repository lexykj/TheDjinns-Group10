from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apis.models import Event, ParkingLot, ParkingSpot, Reservation, Profile


def home(request):
    events = Event.objects.order_by('date')[:4]
    return render(request, 'web/signUp.html', {'events': events})

def reserve(request):
    events = Event.objects.order_by('-date')[:4]
    lots = ParkingLot.objects.order_by('name')
    spots = ParkingSpot.objects.order_by('price')
    return render(request, 'web/reserveSpot.html', {'events': events, 'lots': lots, 'spots': spots})

def selectSpot(request):
    eventId = request.GET['eventCategory']
    event = Event.objects.get(pk=eventId)
    lotId = request.GET['lotCategory']
    lot = ParkingLot.objects.get(pk=lotId)
    spotId = request.GET['spotCategory']
    spot = ParkingSpot.objects.get(pk=spotId)
    print(event)
    return render(request, 'web/reserveSpot.html', {'event': event, 'lot': lot, 'spot': spot})

def pay(request, eventId, spotId):
    event = Event.objects.get(pk=eventId)
    spot = ParkingSpot.objects.get(pk=spotId)
    user = request.user
    spot.spots -= 1
    spot.save()
    user.profile.account_balance -= spot.price
    user.profile.save()
    Reservation.objects.create(uuid=event.id, spot=spot, user=user)
    return redirect('/home')

def loginpage(request):
    return render(request, 'web/login.html')

def signIn(request):
    if request.user.is_authenticated:
        return redirect('/home')
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            message = "Invalid username/password"
    return render(request, 'web/login.html', {'message': message})

def signUp(request):
    if request.user.is_authenticated:
        return redirect('/home')
    message = ""
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                message = "Error creating user"
        else:
            message = "Passwords do not match"
    return render(request, 'web/signUp.html', {'message': message})

def signOut(request):
    logout(request)
    return redirect('/')
        

def main(request):
    events = Event.objects.order_by('date')[:4]
    lots = ParkingLot.objects.order_by('id')
    profile = Profile.objects.all()
    context = {
        'events': events,
        'lots': lots,
        'profile': profile,
    }
    return render(request, 'web/main.html', context)

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

def map(request, id):
    event = Event.objects.all().get(id)
    return render(request, 'web/map.html', {'event': event})