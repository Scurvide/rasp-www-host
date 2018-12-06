from django.urls import path

from . import data_receive, data_view, register, command, base, delete

urlpatterns = [
    path('', base.index, name = 'base'),
    path('send/', data_receive.index, name = 'send'),
    path('register/', register.index, name = 'register'),
    path('command/', command.index, name = 'command'),
    path('command/<client>/<command>', command.command),
    path('data/', data_view.index, name = 'data'),
    path('data/<client>/', data_view.client_data),
    path('delete/', delete.index, name = 'delete'),
    path('delete/<client>/', delete.delete),
]
