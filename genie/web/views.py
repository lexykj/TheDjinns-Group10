from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apis.models import Event, ParkingLot, ParkingSpot, Reservation, Profile
import random
import string

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
    uuid = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    Reservation.objects.create(uuid=uuid, event=event, spot=spot, user=user)
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
            newUser = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=newUser)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                message = "Error creating user"
        else:
            message = "Passwords do not match"
    return render(request, 'web/signUp.html', {'message': message})

def change(request):
    message = ''
    oldPassword = request.POST['oldPass']
    newPassword = request.POST['newPass']
    confirmPassword = request.POST['confNewPass']
    user = request.user
    if user.password == oldPassword:
        if newPassword == confirmPassword:
            user.password = newPassword
            user.save()
        else:
            message = "New passwords do not match"
    else:
        message = "Old password is incorrect"

    # reservations = Reservation.objects.order_by('event')
    # res_list = []
    # for r in reservations:
    #     if r.user == user:
    #         res_list.append(r)    

    # context = {
    #     'email': user.email,
    #     'balance': user.profile.account_balance,
    #     'message': message,
    #     'reservations': res_list,
    # }
    return redirect('/account', message)

def signOut(request):
    logout(request)
    return redirect('/')
        

def main(request):
    events = Event.objects.order_by('date')[:4]
    lots = ParkingLot.objects.order_by('id')
    context = {
        'events': events,
        'lots': lots,
    }
    return render(request, 'web/main.html', context)

def account(request):
    user = request.user
    balance = user.profile.account_balance
    email = user.email
    message = ''
    reservations = Reservation.objects.order_by('event')
    res_list = []
    for r in reservations:
        if r.user == user:
            res_list.append(r)

    context = {
        'balance': balance,
        'email': email,
        'message': message,
        'reservations': res_list,
    }
    return render(request, 'web/account.html', context)

def balance(request):
    funds = request.POST['addFunds']
    user = request.user
    user.profile.account_balance += float(funds)
    user.profile.save()
    return redirect('/account')

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
    event = Event.objects.all().get(id=id)
    return render(request, 'web/map.html', {'event': event})