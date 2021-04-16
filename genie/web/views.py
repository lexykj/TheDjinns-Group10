from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apis.models import Revenue, Event, ParkingLot, ParkingSpot, Reservation, Profile

# import datetime
from django.utils import timezone
from datetime import date, time, datetime
import random
import string

def home(request):
    events = Event.objects.order_by('date')
    upcomingEvents = []
    now = timezone.now()
    for e in events:
        dateStr = e.date
        if not dateStr < now:
            upcomingEvents.append(e)
    context = {
        'events': upcomingEvents[:4],
    }
    return render(request, 'web/signUp.html', context)


def reserve(request):
    allEvents = Event.objects.order_by('-date')
    events = []
    now = timezone.now()
    for e in allEvents:
        if e.date > now:
            events.append(e)
    lots = ParkingLot.objects.order_by('name')
    spots = ParkingSpot.objects.order_by('price')
    reservations = Reservation.objects.order_by('event')

    # Lot-Info Reserve Link Autofill
    preFilledId = request.POST.get('lotId', "")
    if preFilledId != "":
        preFilledLot = ParkingLot.objects.all().get(id=preFilledId)
        preFilledLotName = preFilledLot.name
    else:
        preFilledLot = None
        preFilledLotName = " -Select Lot- "

    # History Reserve Again Autofill
    againLotId = request.POST.get('againLotId', "")
    if againLotId != "":
        againLot = ParkingLot.objects.all().get(id=againLotId)
        againLotName = againLot.name
        againSpotId = request.POST.get('againSpotId', '')
        againSpotType = ParkingSpot.objects.all().get(id=againSpotId)
    else:
        againLot = None
        againLotName = " -Select Lot- "
        againSpotId = ''
        againSpotType = " -Select Parking Type- "

    return render(request, 'web/reserveSpot.html', {'events': events[:10],
                                                    'lots': lots,
                                                    'spots': spots,
                                                    'select': True,
                                                    'preFilledLot': preFilledLot,
                                                    'preFilledLotId': preFilledId,
                                                    'preFilledLotName': preFilledLotName,
                                                    'againLotId': againLotId,
                                                    'againLot': againLot,
                                                    'againLotName': againLotName,
                                                    'againSpotId': againSpotId,
                                                    'againSpotType': againSpotType,
                                                    'reservations': reservations,
                                                    })


def selectSpot(request):
    eventId = request.GET['eventCategory']
    event = Event.objects.get(pk=eventId)
    lotId = request.GET['lotCategory']
    lot = ParkingLot.objects.get(pk=lotId)
    print(lot)
    spotId = request.GET['spotCategory']
    spot = ParkingSpot.objects.get(pk=spotId)
    print(event)
    return render(request, 'web/reserveSpot.html', {'event': event, 'lot': lot, 'spot': spot, 'select': False})


def pay(request, eventId, lotId, spotId):
    event = Event.objects.get(pk=eventId)
    spot = ParkingSpot.objects.get(pk=spotId)
    lot = ParkingLot.objects.get(pk=lotId)
    # try:
    #     revenue = Revenue.objects.get(event)
    # except ObjectDoesNotExist:
    #     revenue = Revenue.objects.create(event=event, lot=lot)
    # revenue.amount += spot.price
    # revenue.save()
    user = request.user
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
    return render(request, 'web/signUp.html', {'message': message, })


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
        'user': user,
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
    theseLots = ParkingLot.objects.filter(event=eventId)
    context = {
        'event': thisEvent,
        'lots': theseLots,
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
    time = request.POST['time']
    description = request.POST['description']
    address = request.POST['address']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']

    fullDate = date + " " + time

    Event.objects.create(name=name, description=description, date=fullDate, address=address, latitude=latitude,
                         longitude=longitude)
    return redirect('/events')


def deleteEvent(request, eventId):
    event = Event.objects.get(pk=eventId)
    event.delete()
    return redirect('/events')


def owners(request):
    return render(request, 'web/ownerManagement.html')


def lots(request):
    user = request.user
    lot_list = ParkingLot.objects.filter(owner=user)
    event_limit = 5
    attendant_limit = 5
    total_spots = [0]*len(lot_list)

    for i in range(len(lot_list)):
        for spot in lot_list[i].parkingspot_set.all():
            total_spots[i] += spot.totalSpots

    data_list = zip(lot_list, total_spots)
    return render(request, 'web/lotManagement.html', {
        'attendant_limit': attendant_limit,
        'data_list': data_list,
        'event_limit': event_limit,
        'lot_list': lot_list,
        'total_spots': total_spots,
    })


def lotEdit(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)

    return render(request, 'web/lotEdit.html')


def info(request):
    # Common needed context
    thisProfile = Profile.objects.get(user_id=request.user.id)

    # Determine whether this is a new lot request or not
    if request.POST.get('registerNewLot') != 'doRegisterLot':
        currentEventId = request.POST.get('eventForLot', 1)
        currentEvent = Event.objects.all().get(id=currentEventId)
        allEventsForLot = []

        # Get lot id from various entry points on main or history
        reservationLotId = request.POST.get('whichCurrentLot', -1)
        whichLotId = request.POST.get('whichLot', -1)
        lotId = request.POST.get('lot', -1)
        pastResId = request.POST.get('pastReservation', -1)
        if reservationLotId != -1:
            thisLot = ParkingLot.objects.all().get(id=reservationLotId)
            allEventsForLot = thisLot.event.all()
        elif whichLotId != -1:
            thisLot = ParkingLot.objects.all().get(id=whichLotId)
            allEventsForLot = thisLot.event.all()
        elif lotId != -1:
            thisLot = ParkingLot.objects.all().get(id=lotId)
            allEventsForLot = thisLot.event.all()

            # Entry point on history
            if pastResId != -1:
                pastReservation = Reservation.objects.all().get(id=pastResId)
                currentEventId = pastReservation.event.id
                currentEvent = Event.objects.all().get(id=currentEventId)

        else:
            # this is a default value that should not be passed
            # TODO: ensure this works as intended and there aren't any associated bugs
            thisLot = ParkingLot.objects.all()[0]
        spots = ParkingSpot.objects.all().filter(lot=thisLot.id)

        context = {
            'isNew': False,
            'currentEvent': currentEvent,
            'lot': thisLot,
            'spots': spots,
            'profile': thisProfile,
            'allEventsForLot': allEventsForLot,
        }

    else:
        newName = request.POST.get('lotName', None)
        newAddress = request.POST.get('lotAddress', None)
        initialEventId = request.POST.get('chooseEvent', 1)
        newOwnerId = request.POST.get('newOwnerId', request.user.id)
        newLat = request.POST.get('latitude', 0.0)
        newLong = request.POST.get('longitude', 0.0)
        newSpotType = request.POST.get('newSpotType', 'Generic')
        newQuantity = request.POST.get('newQuantity', 1)
        newPrice = request.POST.get('newPrice', 10.0)

        # Create new parking lot & parking spot
        thisNewLot = ParkingLot.objects.create(name=newName, address=newAddress, latitude=newLat, longitude=newLong,
                                               owner=User.objects.all().get(id=newOwnerId))
        chosenEvent = Event.objects.all().get(id=initialEventId)
        thisNewLot.event.add(chosenEvent)
        thisNewLot.save()
        thisNewSpot = ParkingSpot.objects.create(spotType=newSpotType, price=newPrice, totalSpots=newQuantity,
                                                 currentEventAvailableSpots=newQuantity, lot=thisNewLot)
        thisNewSpot.save()

        # pass context to template
        context = {
            'isNew': True,
            'currentEvent': chosenEvent,
            'lot': thisNewLot,
            'spots': ParkingSpot.objects.all().filter(lot=thisNewLot.id),
            'profile': thisProfile,
            'allEventsForLot': thisNewLot.event.all()
        }

    return render(request, 'web/lotInfo.html', context)


def map(request, id):
    event = Event.objects.all().get(id=id)
    return render(request, 'web/map.html', {'event': event})


def defaultMap(request):
    return render(request, 'web/defaultMap.html')


def about(request):
    return render(request, 'web/about.html')
