from django.urls import path

from . import data_receive, data_view, register

urlpatterns = [
    path('send/', data_receive.index, name='send'),
    path('register/', register.index, name='register'),
    path('', data_view.index, name = 'view'),
    path('view/', data_view.index, name = 'view'),
    #path('command/<client>/<command>', command.index, name = 'command'),
]
