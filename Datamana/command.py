from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from Datamana.models import Client, Command

# Gets commands for clients
def index( request ):

    context = {
        'clients': Client.objects.all()
    }
    return render( request, 'command.html', context )

# Sets command for client in database
def command( request, client, command ):

    cli = Client.objects.get( name = client )

    for com in cli.command_set.all():
        if com.name == command:
            cli.current_command = command
            cli.save()
            return HttpResponse( 'Success' )

    return HttpResponse( client + ' ' + command )
