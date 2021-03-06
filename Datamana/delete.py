from django.shortcuts import render, redirect
from django.http import HttpRequest
from Datamana.models import Client

# Deletes client and all related data from database

def index( request ):

    context = {
        'clients': Client.objects.all()
    }
    return render( request, 'delete.html', context )

def delete( request, client ):

    cli = Client.objects.get( name = client )
    cli.delete()

    return redirect( 'delete' )
