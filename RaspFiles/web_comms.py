from requests.exceptions import ConnectionError
import json, time, requests

# Options
urlSend     = 'http://raspdatahost.herokuapp.com/send/'      # Url for sending data
urlRegister = 'http://raspdatahost.herokuapp.com/register/'  # Url for registering device
# Local testing
#urlSend     = 'http://192.168.1.107:8000/send/'      # Url for sending data
#urlRegister = 'http://192.168.1.107:8000/register/'  # Url for registering device

timeout     = 5                                      # Request timeout (seconds)
failTimeout = 2                                      # Timeout if connection fails

def postData( clientInfoFile, data, unit, command ):

    # Try to get client info from file
    try:
        with open( clientInfoFile ) as client_info:
            file = json.load(client_info)
    except:
        print( 'No client info found' )
        return False

    # Start session and get csrf token
    try:
        client = requests.session()
        csrf = client.get( urlSend, timeout = timeout ).cookies[ 'csrftoken' ]
    except requests.exceptions.RequestException:
        print( 'Connection failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Construct package
    payload = {
        'secretId': file[ 'secretId' ],
        'measure': file[ 'measure' ],
        'command': command,
        'point': data,
        'unit': unit
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    print( 'Sending data to database...' )
    # Send post and retrieve response
    try:
        resp = client.post( urlSend, data = payload, headers = headers, timeout = timeout )
    except requests.exceptions.RequestException:
        print( 'Post failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Handle response
    if resp.status_code == 200:
        print( 'Datapoint successfully saved to database' )
        content = json.loads(resp.content)
        # Update client info
        with open( clientInfoFile, 'w' ) as client_info:
            json.dump( content, client_info )
        print( 'Client info updated' )
        return True
    else:
        print( resp.content )
        return False


def register( clientInfoFile, commands, graphTypes, secretId = 'None' ):

    # Check if existing client info can be found
    try:
        with open( clientInfoFile ) as client_info:
            file = json.load(client_info)
        if 'secretId' in file:
            secretId = file[ 'secretId' ]
    except:
        print( 'No client info found, requesting new id from the web server...')

    # Start session and get csrf token
    try:
        client = requests.session()
        csrf = client.get( urlRegister, timeout = timeout ).cookies[ 'csrftoken' ]
    except requests.exceptions.RequestException:
        print( 'Connection failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Construct package
    payload = {
        'secretId': secretId,
        'commands': commands,
        'graphTypes': graphTypes
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    # Send post and retrieve response
    try:
        resp = client.post( urlRegister, data = payload, headers = headers, timeout = timeout )
    except requests.exceptions.RequestException:
        print( 'Post failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Handle response
    if resp.status_code == 200:
        content = json.loads(resp.content)
        # Save received info to file
        with open( clientInfoFile, 'w') as client_info:
            json.dump( content, client_info )
        print( 'Client info updated' )
        print( 'Client name: ' + content[ 'name' ] )
        print( 'Current command: ' + content[ 'command' ] )
        return True

    elif resp.status_code == 406:
        print( resp.content )
        return 'Reset'

    else:
        print( resp.content )
        return False
