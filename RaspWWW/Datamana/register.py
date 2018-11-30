from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Datamana.models import Client, Command, Datapoint
from Datamana.syntax_check import syntax_check
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
        passed, msg = syntax_check( payload )
        if passed == False:
            response = HttpResponse( msg )
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
