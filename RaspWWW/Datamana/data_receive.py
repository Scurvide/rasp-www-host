from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Datamana.models import Client, Command, Datapoint
import json

#@csrf_exempt
@ensure_csrf_cookie
def index( request ):

    if request.method == 'POST':
        payload = request.body

        # Check payload data type and load it if json
        try:
            payload = json.loads( payload )
        except ValueError:
            response = HttpResponse( 'No json found in payload.' )
            response.status_code = 400
            return response

        # Syntax check
        if syntax_check(payload) == False:
            response = HttpResponse( 'Syntax Incorrect. name(str, 3-30 char) secretId(str, 10 char) command(str, 3-30 char) point(int or float, <11 char)' )
            response.status_code = 400
            return response

        name = payload[ 'name' ]
        secretId = payload[ 'secretId' ]
        command = payload[ 'command' ]
        point = payload[ 'point' ]

        # Check if client id exists
        try:
            client = Client.objects.get( secretId = secretId )
        except ObjectDoesNotExist:
            response = HttpResponse( 'Client not registered to database' )
            response.status_code = 400
            return response

        # Check if datatype already exists in database
        command = command.lower()
        try:
            com = Command.objects.get( name = command )
        except ObjectDoesNotExist:
            response = HttpResponse( 'Data type not registered to database' )
            response.status_code = 400
            return response

        data = Datapoint.objects.create( client = client, command = com, point = point )

        # Construct response with current command for operation
        response = json.dumps({
            'command': client.current_command,
            'msg':
            'Datapoint successfully saved to database. Client('
            + client.name +
            ') Data type('
            + com.name +
            ') Point('
            + str(data.point) + ')'
            })
        return HttpResponse( response )

    return HttpResponse( "Get Csrf Tokens here!" )


# Syntax check returns True if passed and False if failed
def syntax_check( data ):
    try:
        name = data[ 'name' ]
        secretId = data[ 'secretId' ]
        command = data[ 'command' ]
        point = data[ 'point' ]
    except KeyError:
        return False

    checks = 0

    if isinstance( name, str ):
        if len( name ) < 31 and len( name ) > 2:
            checks += 1

    if isinstance( secretId, str ):
        if len( secretId ) == 10:
            checks += 1

    if isinstance( command, str ):
        if len( command ) < 31 and len( command ) > 2:
            checks += 1

    if isinstance( point, int ) or isinstance( point, float ):
        if len( str( point ) ) <= 10:
            checks += 1

    if checks == 4:
        return True
    return False
