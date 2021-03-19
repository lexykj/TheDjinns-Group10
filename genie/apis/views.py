import json
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Event, ParkingLot, ParkingSpot
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# http://127.0.0.1:8000/api/current_events/?num=5
def get_events(request):
    number = int(request.GET['num'])

    json = {}
    for i, event in enumerate(Event.objects.order_by('-date')[:number]):
        event_json = {}
        for field in event._meta.fields:
            event_json[field.name] = eval('event.'+field.name)
        json[i] = event_json
            

    response = JsonResponse(json)
    response['Access-Control-Allow-Origin'] = '*'
    return response

# http://127.0.0.1:8000/api/map_data/?event_id=5
def get_lots(request):
    event_id = int(request.GET['event_id'])
    event = get_object_or_404(Event, pk=event_id)

    json = {}
    for field in event._meta.fields:
        json[field.name] = eval('event.'+field.name)
    
    lots = {}
    for i, lot in enumerate(ParkingLot.objects.filter(event=event_id)):
        lot_json = {}
        for field in lot._meta.fields:
            if field.name != 'event' and field.name != 'owner':
                lot_json[field.name] = eval('lot.'+field.name)
        lots[i] = lot_json
    json['lots'] = lots

    response = JsonResponse(json)
    response['Access-Control-Allow-Origin'] = '*'
    return response
