from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.home, name='home'),
    path('reserve', views.reserve, name='reserve'),
    path('login', views.loginpage, name='login'),
    path('home', views.main, name='main'),
    path('account', views.account, name='account'),
    path('history', views.history, name='history'),
    path('attendant', views.attendant, name='attendant'),
    path('events', views.events, name='events'),
    path('owners', views.owners, name='owners'),
    path('lots', views.lots, name='lots'),
    path('lot-info', views.info, name='lot-info'),
    path('signIn', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp'),
    path('logout', views.signOut, name='logout'),
    path('map/<int:id>', views.map, name='map')
]