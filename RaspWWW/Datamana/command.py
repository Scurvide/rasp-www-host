from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from Datamana.models import Client, Command

def index( request ):

    context = {
        'clients': Client.objects.all()
    }
    return render( request, 'command.html', context )

def command( request, client, command ):

    cli = Client.objects.get( name = 'Mog' )

    for com in cli.command_set.all():
        if com.name == command:
            cli.current_command = command
            cli.save()
            return redirect( 'command' )

    return HttpResponse( client + ' ' + command )
