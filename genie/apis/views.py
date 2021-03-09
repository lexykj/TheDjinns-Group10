from django.http import JsonResponse

from .models import Event, ParkingLot, ParkingSpot


def get_events(request):
    try:
        number = int(request.GET['num'])
        events = Event.objects.order_by('-date')[:number]

        response = JsonResponse(events)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = JsonResponse({"error": "Invalid unit conversion request"})
        response['Access-Control-Allow-Origin'] = '*'
        return response


def get_lots(request):
    pass
