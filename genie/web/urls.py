from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.home, name='home'),
    path('reserve', views.reserve, name='reserve'),
    path('login', views.login, name='login'),
    path('home', views.main, name='main'),
    path('account', views.account, name='account'),
    path('history', views.history, name='history'),
    path('attendant', views.attendant, name='attendant'),
    path('events', views.events, name='events'),
    path('owners', views.owners, name='owners'),

]