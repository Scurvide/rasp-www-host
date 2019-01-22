from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie
from Datamana.models import Client, Command, Datapoint
from Datamana.syntax_check import syntax_check
import json, random, string

# Registering is done by sending a POST message that includes
# desired name, secretId as None and list of commands client can use.
# Generates clients random name (if necessary) and secretId,
# which is used to identify the client when it sends data to server.
# Registering new commands is done by sending a POST message that
# includes name, secretId, and new list of commands.
# Responds to client with client info that the client should
# include with any future POST messages to server.
# Data in POST messages should be in json format.

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
        commands = payload[ 'commands' ]
        graphTypes = payload[ 'graphTypes' ]

        # Check if secretId and name exists. If not, create randoms
        if secretId == 'None':
            # Create random secretId and name
            secretId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(secretIdLen))
            name = ''.join(random.choice(string.ascii_letters) for _ in range(randomNameLen))
            # Try to create a new client object until both secretId and name
            # are unique
            success = False
            while success == False:
            # Create new client object
                try:
                    client = Client.objects.create( name = name, secretId = secretId, current_command = commands[0] )
                    success = True
                except IntegrityError:
                    # Name or id needs to be unique
                    secretId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(secretIdLen))
                    name = ''.join(random.choice(string.ascii_letters) for _ in range(randomNameLen))
        else:
            try:
                client = Client.objects.get( secretId = secretId )
            except ObjectDoesNotExist:
                response = HttpResponse( 'Secret Id not valid, delete client info file to assign new Id' )
                response.status_code = 406
                return response

        # Create commands if needed
        i = 0
        for command in commands:
            command = command.lower()
            try:
                com = Command.objects.get( name = command )
            except ObjectDoesNotExist:
                com = Command.objects.create( name = command, graphType = graphTypes[i] )
            com.client.add( client )
            i += 1

        # Returns client info and first listed command as command
        response = json.dumps({
            'secretId': client.secretId,
            'name': client.name,
            'command': client.current_command,
            'measure': client.measure,
            'autoMeasure': client.autoMeasure
            })
        return HttpResponse( response )

    return HttpResponse( "Get Csrf Tokens here!" )
