from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Datamana.models import Client, Datatype, Datapoint
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
            response = HttpResponse( 'No json found in payload. Request Ip: ' + ip )
            response.status_code = 400
            return response

        # Syntax check
        if syntax_check(payload) == False:
            response = HttpResponse( 'Syntax Incorrect. name(str, 3-30 char) id(str, 10 char) datatype(str, 3-30 char) point(int or float, <11 char)' )
            response.status_code = 400
            return response

        name = payload[ 'name' ]
        secretid = payload[ 'secretid' ]
        datatype = payload[ 'datatype' ]
        point = payload[ 'point' ]

        # Check if client id exists
        try:
            client = Client.objects.get( secretid = secretid )
        except ObjectDoesNotExist:
            # If not, Create new client model
            try:
                client = Client.objects.create( name = name, secretid = secretid, ip = ip )
            except IntegrityError:
                response = HttpResponse ( 'Name needs to be unique' )
                response.status_code = 400
                return response

        # Check if datatype already exists in database
        datatype = datatype.lower()
        try:
            type = Datatype.objects.get( name = datatype )
        except ObjectDoesNotExist:
            # If not, Create new datatype model
            type = Datatype.objects.create( name = datatype )
            type.client.add( client )
            type.save()

        Datapoint.objects.create( client = client, datatype = type, point = point )

        # Check if Ip address the same as in database, update if not
        ip_updated = False
        if client.ip != ip:
            client.ip = ip
            client.save()
            ip_updated = True

        return HttpResponse(
            'Datapoint successfully saved to database. Name('
            + name +
            ') Data collection mode('
            + client.datamode +
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
        secretid = data[ 'secretid' ]
        datatype = data[ 'datatype' ]
        point = data[ 'point' ]
    except KeyError:
        return False

    checks = 0

    if isinstance( name, str ):
        if len( name ) < 31 and len( name ) > 2:
            checks += 1

    if isinstance( secretid, str ):
        if len( secretid ) == 10:
            checks += 1

    if isinstance( datatype, str ):
        if len( datatype ) < 31 and len( datatype ) > 2:
            checks += 1

    if isinstance( point, int ) or isinstance( point, float ):
        if len( str( point ) ) <= 10:
            checks += 1

    if checks == 4:
        return True
    return False
