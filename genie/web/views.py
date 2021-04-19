from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from apis.models import Revenue, Event, ParkingLot, ParkingSpot, Reservation, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q


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
    revenueList = Revenue.objects.order_by('lot')
    revenueAmount=0
    for rev in revenueList:
        if rev.lot.owner == user:
            revenueAmount += rev.amount
    context = {
        'user': user,
        'balance': balance,
        'email': email,
        'message': message,
        'reservations': res_list,
        'pastReservations': pastRes[:4],
        'currentReservations': currRes,
        'revenue': revenueAmount
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
    event = Event.objects.all().get(id=eventId)
    context = {
        'event': event,
        'checked_in': None
    }
    if 'query' in request.POST:
        context['checked_in'] = False
        uuid = request.POST['query']

        for res in Reservation.objects.filter(uuid=uuid):
            if res.event == event:
                for lot in request.user.profile.attendant_for.all():
                    if lot == res.spot.lot:
                        context['checked_in'] = True
                        res.checked_in = True
                        res.save()
                        context['user'] = res.user
                        context['spot'] = res.spot.spotType
        
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
    user = request.user
    profile = Profile.objects.all().get(user=user)
    # Ensure user is not bypassing permissions
    if not profile.is_admin:
        return redirect('/home')

    revokeOwner = request.POST.get('revokeOwner', -1)
    makeAdmin = request.POST.get('makeAdmin', -1)
    if revokeOwner != -1:
        revokedUser = User.objects.all().get(id=revokeOwner)
        revokedProfile = Profile.objects.all().get(user=revokedUser)
        previousLots = ParkingLot.objects.all().filter(owner=revokedUser)
        revokedProfile.is_owner = 0
        revokedProfile.save()
        # Transfer ownership to current admin
        for lot in previousLots:
            lot.owner = user
    elif makeAdmin != -1:
        pass

    allOwners = Profile.objects.all().filter(is_owner=1)
    context = {
        'allOwners': allOwners,
    }
    return render(request, 'web/ownerManagement.html', context)


def lots(request):
    # Determine whether this request is from the ownerManagement page on behalf of an admin
    thisOwner = request.POST.get('thisOwner', -1)
    if thisOwner != -1:
        user = User.objects.all().get(username=thisOwner)
    else:
        user = request.user

    lot_list = ParkingLot.objects.filter(owner=user)
    event_limit = 5
    attendant_limit = 5
    total_spots = [0]*len(lot_list)
    current_date = timezone.now()

    for i in range(len(lot_list)):
        for spot in lot_list[i].parkingspot_set.all():
            total_spots[i] += spot.totalSpots

    data_list = zip(lot_list, total_spots)
    return render(request, 'web/lotManagement.html', {
        'attendant_limit': attendant_limit,
        'current_date': current_date,
        'data_list': data_list,
        'event_limit': event_limit,
        'lot_list': lot_list,
        'total_spots': total_spots,
        'user': user,
    })


def lotEdit(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    user = request.user
    # event_list = parkingLot.event.order_by('-date')
    event_list, other_event_list, attendant_list, other_attendants, spot_list, total_spots = get_lot_details(parkingLot)

    return render(request, 'web/lotEdit.html', {
        'attendant_list': attendant_list,
        'other_attendant_list': other_attendants,
        'event_list': event_list,
        'other_event_list': other_event_list,
        'parkingLot': parkingLot,
        'spot_list': spot_list,
        'total_spots': total_spots,
    })


def get_lot_details(parkingLot):
    all_events = Event.objects.order_by('date')
    event_list = []
    other_events = []
    now = timezone.now()
    for event in all_events:
        if event.date > now:
            if Event.objects.filter(id=event.id).filter(parkinglot__id=parkingLot.id).exists():
                event_list.append(event)
            else:
                other_events.append(event)
    attendant_list = parkingLot.profile_set.all()
    other_attendants = Profile.objects.all().exclude(attendant_for__id=parkingLot.id)
    spot_list = parkingLot.parkingspot_set.all()
    total_spots = 0

    for spot in spot_list:
        total_spots += spot.totalSpots

    return event_list, other_events, attendant_list, other_attendants, spot_list, total_spots


def renderLotEdit(request, parkingLot, errorKey, errorMessage):
    event_list, other_events, attendant_list, other_attendants, spot_list, total_spots = get_lot_details(parkingLot)
    if errorKey and errorMessage:
        return render(request, 'web/lotEdit.html', {
            'parkingLot': parkingLot,
            errorKey: errorMessage,
            'event_list': event_list,
            'other_event_list': other_events,
            'attendant_list': attendant_list,
            'other_attendant_list': other_attendants,
            'spot_list': spot_list,
            'total_spots': total_spots,
        })
    return render(request, 'web/lotEdit.html', {
        'parkingLot': parkingLot,
        'event_list': event_list,
        'other_event_list': other_events,
        'attendant_list': attendant_list,
        'other_attendant_list': other_attendants,
        'spot_list': spot_list,
        'total_spots': total_spots,
    })


def lot_change_name(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    try:
        name = request.POST['name']
        if name != "":
            parkingLot.name = name
            parkingLot.save()
        else:
            return renderLotEdit(request, parkingLot, 'name_error_message', "Name not changed: Empty text field")
    except(KeyError, ParkingLot.DoesNotExist):

        return renderLotEdit(request, parkingLot, 'name_error_message', "Name was not changed")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_change_address(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    try:
        address = request.POST['address']
        if address != "":
            parkingLot.address = address
            parkingLot.save()
        else:
            return renderLotEdit(request, parkingLot, 'address_error_message', "Address not changed: Empty text field")

    except(KeyError, ParkingLot.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'address_error_message', "Address was not changed")

    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_delete_events(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    event_list = Event.objects.filter(parkinglot__id=parkingLot.id)
    try:
        for event in event_list:
            if str(event.id) in request.POST:
                parkingLot.event.remove(event)
                parkingLot.save()
    except(KeyError, Event.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'events_error_message', "No events deleted: no items selected")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_add_events(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    event_list = Event.objects.all()
    try:
        for event in event_list:
            if str(event.id) in request.POST:
                parkingLot.event.add(event)
                parkingLot.save()
    except(KeyError, Event.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'events_error_message', "No events added: no items selected")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_delete_attendants(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    attendant_list = parkingLot.profile_set.all()
    try:
        for attendant in attendant_list:
            if str(attendant.id) in request.POST:
                attendant.attendant_for.remove(parkingLot)
                attendant.save()
                # TODO: check if they're an attendant for any other lot. If not, switch "is_attendant" to false.
    except(KeyError, Event.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'attendants_error_message', "No events deleted: no items selected")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_add_attendants(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    attendant_list = Profile.objects.all()
    try:
        for attendant in attendant_list:
            if str(attendant.id) in request.POST:
                attendant.is_attendant = True
                attendant.attendant_for.add(parkingLot)
                attendant.save()
    except(KeyError, Event.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'attendants_error_message', "No Attendant added: no items selected")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_delete_spot(request, spot_id):
    parkingSpot = get_object_or_404(ParkingSpot, pk=spot_id)
    parkingLot = ParkingLot.objects.get(parkingspot__id=parkingSpot.id)
    try:
        # parkingLot.parkingspot_set.remove(parkingSpot)
        parkingSpot.delete()
        parkingLot.save()
    except(KeyError, ParkingSpot.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'spot_error_message', "Parking spot not deleted")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_edit_spot(request, spot_id):
    parkingSpot = get_object_or_404(ParkingSpot, pk=spot_id)
    parkingLot = ParkingLot.objects.get(parkingspot__id=parkingSpot.id)
    try:
        type = request.POST['type']
        quantity = request.POST['quantity']
        price = request.POST['price']
        if type != "":
            parkingSpot.spotType = type
        if quantity != "":
            parkingSpot.totalSpots = quantity
        if price != "":
            parkingSpot.price = price
        parkingSpot.save()
    except(KeyError, ParkingSpot.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'spot_error_message', "Unable to Edit Parking Spot")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def lot_add_spot(request, parkingLot_id):
    parkingLot = get_object_or_404(ParkingLot, pk=parkingLot_id)
    try:
        parkingLot.parkingspot_set.create(
            spotType=request.POST['type'],
            price=request.POST['price'],
            totalSpots=request.POST['quantity'],
            lot=parkingLot
        )
    except(KeyError, ParkingSpot.DoesNotExist):
        return renderLotEdit(request, parkingLot, 'add_spot_error_message', "Unable to add Parking Spot(s)")
    else:
        return HttpResponseRedirect(reverse('web:lotEdit', args=(parkingLot.id,)))


def info(request):
    # Common needed context
    thisProfile = Profile.objects.get(user_id=request.user.id)

    # Determine whether this is a new lot request or not
    if request.POST.get('registerNewLot') != 'doRegisterLot':
        currentEventId = request.POST.get('eventForLot', -1)
        if currentEventId == -1:
            currentEventId = request.POST.get('passEvent', -1)
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
            thisLot = ParkingLot.objects.all()[0]
        spots = ParkingSpot.objects.all().filter(lot=thisLot.id)
        reservations = Reservation.objects.all().filter(event=currentEvent)
        reservationTotals = {}
        for spot in spots:
            reservationTotals[spot] = spot.totalSpots
            for reservation in reservations:
                if reservation.spot == spot:
                    reservationTotals[spot] -= 1
        context = {
            'isNew': False,
            'currentEvent': currentEvent,
            'lot': thisLot,
            'spots': spots,
            'profile': thisProfile,
            'allEventsForLot': allEventsForLot,
            'allReservations': reservations,
            'availableSpots': reservationTotals,
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
        Revenue.objects.create(event=chosenEvent, lot=thisNewLot, amount=0.0)

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
