from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Datamana.models import Client, Command, Datapoint
import json, random, string

# Options
randomNameLen   = 5     # Random placeholder name length
secretIdLen     = 10    # Secret id length

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
            response = HttpResponse( 'Syntax Incorrect. name(str, 3-30 char) secretId(str, 10 char) commands(array of str, 3-30 char)' )
            response.status_code = 400
            return response

        secretId = payload[ 'secretId' ]
        name = payload[ 'name' ]
        commands = payload[ 'commands' ]

        # Check if secretId and name exists. If not, create randoms
        if secretId == 'None':
            # Create random secretId
            secretId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(secretIdLen))
            if name == 'None':
                # Create name
                name = ''.join(random.choice(string.ascii_letters) for _ in range(randomNameLen))
            success = False
            while success == False:
            # Create new client object
                try:
                    client = Client.objects.create( name = name, secretId = secretId, current_command = commands[0] )
                    success = True
                except IntegrityError:
                    # Name or id needs to be unique
                    name = ''.join(random.choice(string.ascii_letters) for _ in range(randomNameLen))
                    secretId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(secretIdLen))
        else:
            try:
                client = Client.objects.get( secretId = secretId )
            except ObjectDoesNotExist:
                response = HttpResponse( 'Secret Id not valid, use None to assign new Id' )
                response.status_code = 400
                return response
            try:
                client.name = name
            except IntegrityError:
                response = HttpResponse( 'Name already in use' )
                response.status_code = 400
                return response

        # Create commands if needed
        for command in commands:
            command = command.lower()
            try:
                com = Command.objects.get( name = command )
            except ObjectDoesNotExist:
                com = Command.objects.create( name = command )
            com.client.add( client )

        # Returns client info and first listed command as command
        response = json.dumps({
            'name': client.name,
            'secretId': client.secretId,
            'command': client.current_command
            })
        return HttpResponse( response )

    return HttpResponse( "Get Csrf Tokens here!" )

# Syntax check returns True if passed and False if failed
def syntax_check( data ):
    try:
        name = data[ 'name' ]
        secretId = data[ 'secretId' ]
        commands = data[ 'commands' ]
    except KeyError:
        return False

    checks = 0

    if isinstance( name, str ):
        if len( name ) < 31 and len( name ) > 2:
            checks += 1

    if isinstance( secretId, str ):
        if len( secretId ) == 10 or secretId == 'None':
            checks += 1

    passed = True
    for command in commands:
        if isinstance( command, str ):
            if len( command ) < 31 and len( command ) > 2:
                checks += 1
    checks -= len(commands) - 1

    if checks == 3:
        return True
    return False
