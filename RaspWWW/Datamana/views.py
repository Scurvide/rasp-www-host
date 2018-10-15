from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Datamana.models import Raspi, Datapoint
import json

@ensure_csrf_cookie
#@csrf_exempt
def index( request ):

    if request.method == 'POST':
        payload = request.body
        ip = request.META[ 'REMOTE_ADDR' ]
        # Use below instead when online... maybe?
        # ip = request.META[ 'HTTP_X_FORWARDED_FOR' ]

        # Check payload data type and load it if json
        try:
            payload = json.loads( payload )
        except ValueError:
            return HttpResponse( 'No json found in payload. Request Ip: ' + ip )

        # Syntax check
        if syntax_check(payload) == False:
            return HttpResponse( 'Syntax Incorrect. name(str max 30 char) type(distance or instance) point(int or float and max 10 char)' )

        name = payload[ 'name' ]
        type = payload[ 'type' ]
        point = payload[ 'point' ]

        # Check if Raspi name already exists in database
        if name != '':
            try:
                client = Raspi.objects.get( name = name )
            except ObjectDoesNotExist:
                # If not, Create new raspi model
                client = Raspi.objects.create( name = name, ip = ip )
        else:
            return HttpResponse( 'Client name not found in payload', status_code = 400 )

        if type == 'instance':
            point = 1
        if type == 'distance':
            point = round(point, 2)

        Datapoint.objects.create( client = client, type = type, point = point )

        # Check if Ip address the same as in database, update if not
        ip_updated = False
        if client.ip != ip:
            client.ip = ip
            client.save()
            ip_updated = True

        return HttpResponse(
            'Datapoint successfully saved to database. Name('
            + name +
            ') Request Ip('
            + ip +
            ') Ip updated('
            + str(ip_updated) +
            ') Point('
            + str(point) + ')' )

    return HttpResponse( "Get Csrf Tokens here!" )


# Syntax check returns True if passed and False if failed
def syntax_check( data ):
    try:
        name = data[ 'name' ]
        type = data[ 'type' ]
        point = data[ 'point' ]
    except KeyError:
        return False

    checks = 0

    if isinstance( name, str ):
        if len( name ) <= 30:
            checks += 1

    if type == 'instance' or type == 'distance':
        checks += 1

    if isinstance( point, int ) or isinstance( point, float ):
        if len( str( point ) ) <= 10:
            checks += 1

    if checks == 3:
        return True
    return False
