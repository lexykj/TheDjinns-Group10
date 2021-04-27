from django.urls import path

from . import views

urlpatterns = [
    path('current_events/', views.get_events, name='current_events'),
    path('map_data/', views.get_lots, name='map_data'),
    path('lot_data/', views.get_lot_data, name='lot_data')
]