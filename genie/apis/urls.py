from django.urls import path

from . import views

urlpatterns = [
    path('current_events/', views.get_events, name='current_events'),
    path('map_data/', views.get_lots, name='map_data')
]