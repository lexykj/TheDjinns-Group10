from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.home, name='home'),
    path('reserve', views.reserve, name='reserve'),
    path('selectSpot', views.selectSpot, name='selectSpot'),
    path('pay/<int:eventId>/<int:lotId>/<int:spotId>', views.pay, name='pay'),
    path('login', views.loginpage, name='login'),
    path('change-password', views.change, name='change-password'),
    path('home', views.main, name='main'),
    path('account', views.account, name='account'),
    path('account/<str:message>', views.account, name='account'),
    path('balance', views.balance, name='balance'),
    path('history', views.history, name='history'),
    path('attendant', views.attendant, name='attendant'),
    path('events', views.events, name='events'),
    path('add-event', views.addEvent, name='add-event'),
    path('delete-event/<int:eventId>', views.deleteEvent, name='delete-event'),
    path('owners', views.owners, name='owners'),
    path('lots', views.lots, name='lots'),
    path('lotEdit/<int:parkingLot_id>', views.lotEdit, name='lotEdit'),
    path('lot_name/<int:parkingLot_id>', views.change_name, name='change_name'),
    path('lot_address/<int:parkingLot_id>', views.change_address, name='change_address'),
    path('lot-info', views.info, name='lot-info'),
    path('signIn', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp'),
    path('logout', views.signOut, name='logout'),
    path('map/<int:id>', views.map, name='map'),
    path('map/default', views.defaultMap, name='defaultMap'),
    path('about', views.about, name='about'), 
]

