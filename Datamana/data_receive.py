from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from Datamana.models import Client, Command, Datapoint
from Datamana.syntax_check import syntax_check
import json

# Receives data from clients via POST messages
# and stores it to database. Responds to client with
# saved data points information.
# Data in POST messages should be in json format.

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
        command = payload[ 'command' ]
        point = payload[ 'point' ]
        unit = payload[ 'unit' ]
        measure = payload[ 'measure' ]

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

        # Create new data point
        data = Datapoint.objects.create( client = client, command = com, point = point, unit = unit )

        # If measure was true, set it to false
        if measure == True:
            client.measure = False
            client.save()

        # Construct response with current command for operation
        response = json.dumps({
            'secretId': client.secretId,
            'name': client.name,
            'command': client.current_command,
            'measure': client.measure,
            'autoMeasure': client.autoMeasure
            #'msg':
            #'Datapoint successfully saved to database. Client('
            #+ client.name +
            #') Point('
            #+ str(data.point) + data.unit + ')'
            })
        return HttpResponse( response )

    return HttpResponse( "Get Csrf Tokens here!" )
