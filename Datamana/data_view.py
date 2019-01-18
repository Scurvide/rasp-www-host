from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from Datamana.models import Client, Command, Datapoint

# Options
dataPointsShown = 20

def index( request ):

    context = {
        'clients': Client.objects.all()
    }
    return render( request, 'data_clients.html', context )

# Collects client data for viewing
def client_data( request, client ):

    cli = Client.objects.get( name = client )
    allDataPoints = Datapoint.objects.filter( client = cli )
    commands = Command.objects.filter( client = cli )

    data = []
    for com in commands:
        if com.name == 'stop':
            continue
        data.append( allDataPoints.filter( command = com ).order_by('-datetime')[:dataPointsShown][::-1] )

    context = {
        'data': data
    }
    return render( request, 'data.html', context )
