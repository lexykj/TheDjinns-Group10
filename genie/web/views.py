from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from apis.models import Event, ParkingLot, ParkingSpot, Reservation, Profile

# import datetime
from django.utils import timezone
import random
import string

def home(request):
    events = Event.objects.order_by('date')[:4]
    return render(request, 'web/signUp.html', {'events': events,})

def reserve(request):
    allEvents = Event.objects.order_by('-date')
    events = []
    now = timezone.now()
    for e in allEvents:
        if e.date > now:
            events.append(e)
    lots = ParkingLot.objects.order_by('name')
    spots = ParkingSpot.objects.order_by('price')
    return render(request, 'web/reserveSpot.html', {'events': events[:10], 'lots': lots, 'spots': spots, 'select': True})

def selectSpot(request):
    eventId = request.GET['eventCategory']
    event = Event.objects.get(pk=eventId)
    lotId = request.GET['lotCategory']
    lot = ParkingLot.objects.get(pk=lotId)
    spotId = request.GET['spotCategory']
    spot = ParkingSpot.objects.get(pk=spotId)
    print(event)
    return render(request, 'web/reserveSpot.html', {'event': event, 'lot': lot, 'spot': spot, 'select': False})

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
    return render(request, 'web/signUp.html', {'message': message,})

def change(request):
    message = ''
    oldPassword = request.POST['oldPass']
    newPassword = request.POST['newPass']
    confirmPassword = request.POST['confNewPass']
    user = request.user
    username = user.username
    if user.check_password(oldPassword):
        if newPassword == confirmPassword:
            user.set_password(newPassword)
            user.save()
            return redirect('/login')
        else:
            message = "New passwords do not match"
    else:
        message = "Old password is incorrect"
    return redirect('/account/' + message)

def signOut(request):
    logout(request)
    return redirect('/')
        

def main(request):
    events = Event.objects.order_by('date')
    upcomingEvents = []
    lots = ParkingLot.objects.order_by('id')
    user = request.user
    thisProfile = Profile.objects.get(user_id=user.id)
    allReservations = Reservation.objects.order_by('event')
    res_list = []
    pastRes = []
    currRes = []
    now = timezone.now()
    for r in allReservations:
        if r.user == user:
            dateStr = r.event.date
            if dateStr < now:
                pastRes.append(r)
            else:
                currRes.append(r)
            res_list.append(r)
    for e in events:
        dateStr = e.date
        if not dateStr < now:
            upcomingEvents.append(e)
    context = {
        'events': events,
        'lots': lots,
        'user': user,
        'profile': thisProfile,
        'myReservations': res_list,
        'pastReservations': pastRes[:4],
        'currentReservations': currRes,
        'upcomingEvents': upcomingEvents[:4],
    }
    return render(request, 'web/main.html', context)

def account(request, message=""):
    user = request.user
    balance = user.profile.account_balance
    email = user.email
    reservations = Reservation.objects.order_by('event')
    res_list = []
    pastRes = []
    currRes = []
    now = timezone.now()
    for r in reservations:
        if r.user == user:
            dateStr = r.event.date
            if dateStr < now:
                pastRes.append(r)
            else:
                currRes.append(r)
            res_list.append(r)
    context = {
        'balance': balance,
        'email': email,
        'message': message,
        'reservations': res_list,
        'pastReservations': pastRes[:4],
        'currentReservations': currRes,
    }
    return render(request, 'web/account.html', context)

def balance(request):
    funds = request.POST['addFunds']
    user = request.user
    user.profile.account_balance += float(funds)
    user.profile.save()
    return redirect('/account')

def history(request):
    user = request.user
    allReservations = Reservation.objects.order_by('event')
    res_list = []
    pastRes = []
    currRes = []
    now = timezone.now()
    for r in allReservations:
        if r.user == user:
            dateStr = r.event.date
            if dateStr < now:
                pastRes.append(r)
            else:
                currRes.append(r)
            res_list.append(r)
    context = {
        'myReservations': res_list,
        'pastReservations': pastRes,
        'currentReservations': currRes,
    }
    return render(request, 'web/pastReservations.html', context)

def attendant(request):
    eventId = request.POST['event']
    thisEvent = Event.objects.all().get(id=eventId)
    context = {
        'event': thisEvent,
    }
    return render(request, 'web/attendant.html', context)

def events(request):
    allEvents = Event.objects.order_by('-date')
    events = []
    now = timezone.now()
    for e in allEvents:
        if e.date > now:
            events.append(e)
    context = {
        'events': events,
    }
    return render(request, 'web/eventManagement.html', context)

def addEvent(request):
    name = request.POST['name']
    date = request.POST['date']
    description = request.POST['description']
    address = request.POST['address']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    Event.objects.create(name=name, description=description, date=date, address=address, latitude=latitude, longitude=longitude)
    return redirect('/events')

def deleteEvent(request, eventId):
    event = Event.objects.get(pk=eventId)
    event.delete()
    return redirect('/events')

def owners(request):
    return render(request, 'web/ownerManagement.html')

def lots(request):
    return render(request, 'web/lotManagement.html')

def info(request):
    thisProfile = Profile.objects.get(user_id=request.user.id)
    currentEventId = request.POST.get('eventForLot', 1)
    spots = ParkingSpot.objects.all().filter(lot=currentEventId)
    currentEvent = Event.objects.all().get(id=currentEventId)
    allEventsForLot = []

    # Get lot id from various entry points on main
    reservationLotId = request.POST.get('whichCurrentLot', -1)
    whichLotId = request.POST.get('whichLot', -1)
    lotId = request.POST.get('lot', -1)
    if reservationLotId != -1:
        thisLot = ParkingLot.objects.all().get(id=reservationLotId)
        allEventsForLot = thisLot.event.all()
    elif whichLotId != -1:
        thisLot = ParkingLot.objects.all().get(id=whichLotId)
        allEventsForLot = thisLot.event.all()
    elif lotId != -1:
        thisLot = ParkingLot.objects.all().get(id=lotId)
        allEventsForLot = thisLot.event.all()
    else:
        thisLot = None

    context = {
        'currentEvent': currentEvent,
        'lot': thisLot,
        'spots': spots,
        'profile': thisProfile,
        'allEventsForLot': allEventsForLot,
    }
    return render(request, 'web/lotInfo.html', context)

def map(request, id):
    event = Event.objects.all().get(id=id)
    return render(request, 'web/map.html', {'event': event})

def defaultMap(request):
    return render(request, 'web/defaultMap.html')

def about(request):
    return render(request, 'web/about.html')

