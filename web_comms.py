from requests.exceptions import ConnectionError
import json, time, requests

# Options
urlSend     = 'http://192.168.1.107:8000/send/'      # Url for sending data
urlRegister = 'http://192.168.1.107:8000/register/'  # Url for registering device
timeout     = 20                                     # Request timeout (seconds)
failTimeout = 2                                      # Timeout if connection fails

def postData( data, unit = '' ):

    # Try to get client info from file
    try:
        with open('client_info.json') as client_info:
            file = json.load(client_info)
    except:
        print( 'No client info found' )
        return False

    # Start session and get csrf token
    try:
        client = requests.session()
    except ConnectionError:
        print( 'Connection failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False
    csrf = client.get( urlSend ).cookies[ 'csrftoken' ]

    # Construct package
    payload = {
        'name': file[ 'name' ],
        'secretId': file[ 'secretId' ],
        'command': file[ 'command' ],
        'point': data,
        'unit': unit
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    print( 'Sending data to database...' )
    # Send post and retrieve response
    try:
        resp = client.post( urlSend, data = payload, headers = headers, timeout = timeout )
    except ConnectionError:
        print( 'Post failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Handle response
    if resp.status_code == 200:
        content = json.loads(resp.content)
        print( content[ 'msg' ] )
        # Save possible new command
        if content[ 'command' ] != file[ 'command' ]:
            file[ 'command' ] = content[ 'command' ]
            with open('client_info.json', 'w') as client_info:
                json.dump( file, client_info )
            print ( 'New command received: ' + file[ 'command' ] )
        return True
    else:
        print( resp.content )
        return False


def register( commands, name = 'None', secretId = 'None' ):

    # Check if existing client info can be found
    try:
        with open('client_info.json') as client_info:
            file = json.load(client_info)
        if 'name' in file and 'secretId' in file:
            name = file[ 'name' ]
            secretId = file[ 'secretId' ]
    except:
        print( 'No client info found, requesting new id from the web server...')

    # Start session and get csrf token
    try:
        client = requests.session()
    except ConnectionError:
        print( 'Connection failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False
    csrf = client.get( urlRegister ).cookies[ 'csrftoken' ]

    # Construct package
    payload = {
        'name': name,
        'secretId': secretId,
        'commands': commands
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    # Send post and retrieve response
    try:
        resp = client.post( urlRegister, data = payload, headers = headers, timeout = timeout )
    except ConnectionError:
        print( 'Post failed. Waiting ' + str( failTimeout ) + ' seconds before continuing...' )
        time.sleep( failTimeout )
        return False

    # Handle response
    if resp.status_code == 200:
        content = json.loads(resp.content)
    else:
        print( resp.content )
        return False

    # Check that data exists and save it
    if 'name' in content and 'secretId' in content and 'command' in content:
        if content[ 'name' ] != '' and content[ 'secretId' ] != '' and content[ 'command' ] != '':
            with open('client_info.json', 'w') as client_info:
                json.dump( content, client_info )
            print( 'Client info update successful' )
            print( 'Current command: ' + content[ 'command' ] )
            return True
    print( 'Client info update unsuccessful' )
    return False
