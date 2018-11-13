from django.urls import path

from . import data_receive, data_view, register, command

urlpatterns = [
    path('send/', data_receive.index, name='send'),
    path('register/', register.index, name='register'),
    path('command/', command.index, name='command'),
    path('command/<client>/<command>', command.command),
    path('', data_view.index, name = 'view'),
    path('view/', data_view.index, name = 'view'),
]
