from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from Datamana.models import Client, Command, Datapoint

# Sets measure request for client if not set already
def index( request, client ):

    try:
        cli = Client.objects.get( name = client )
    except ObjectDoesNotExist:
        response = HttpResponse( 'No such client found' )
        response.status_code = 404
        return response

    if cli.measure == False:
        cli.measure = True
        cli.save()

    return HttpResponse( 'Measure request set' )

# Toggles measuring to be automatic
def auto( request, client ):

    try:
        cli = Client.objects.get( name = client )
    except ObjectDoesNotExist:
        response = HttpResponse( '404' )
        response.status_code = 404
        return response

    setValue = cli.autoMeasure
    if setValue == False:
        cli.autoMeasure = True
        cli.save()
        return HttpResponse( 'Auto: On' )
    else:
        cli.autoMeasure = False
        cli.save()
        return HttpResponse( 'Auto: Off' )

def auto_status( request, client ):

    try:
        cli = Client.objects.get( name = client )
    except ObjectDoesNotExist:
        response = HttpResponse( '404' )
        response.status_code = 404
        return response

    setValue = cli.autoMeasure
    if setValue == False:
        return HttpResponse( 'Auto: Off' )
    else:
        return HttpResponse( 'Auto: On' )
