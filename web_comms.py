import json, time, requests

# Options
urlSend     = 'http://192.168.1.107:8000/send/'      # Url for sending data
urlRegister = 'http://192.168.1.107:8000/register/'  # Url for registering device

def postData( command, data ):

    # Start session and get csrf token
    client = requests.session()
    csrf = client.get( urlSend ).cookies[ 'csrftoken' ]

    # Get client info from file
    with open( 'client_info.json' ) as client_info:
        file = json.load(client_info)

    try:
        with open('client_info.json') as client_info:
            file = json.load(client_info)
        if 'name' in file and 'secretId' in file:
            print( 'Client info found, adding to request' )
    except:
        print( 'No client info found' )
        return False


    # Construct package
    payload = {
        'name': file[ 'name' ],
        'secretId': file[ 'secretId' ],
        'command': command,
        'point': data
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    # Send post and retrieve response
    resp = client.post( urlSend, data = payload, headers = headers )

    # Handle response
    if resp.status_code == 200:
        print( resp.content )
        return True
    else:
        print( resp.content )
        return False


def register( commands, name = 'None', secretId = 'None' ):

    # Start session and get
    client = requests.session()
    csrf = client.get( urlRegister ).cookies[ 'csrftoken' ]

    try:
        with open('client_info.json') as client_info:
            file = json.load(client_info)
        if 'name' in file and 'secretId' in file:
            name = file[ 'name' ]
            secretId = file[ 'secretId' ]
            print( 'Client info found, adding to request' )
    except:
        print( 'No client info found, requesting new id from the web server...')

    # Construct package
    payload = {
        'name': name,
        'secretId': secretId,
        'commands': commands
        }
    payload = json.dumps( payload )
    headers = { 'X-CSRFToken': csrf }

    # Send post and retrieve response
    resp = client.post( urlRegister, data = payload, headers = headers )

    # Handle response
    if resp.status_code == 200:
        content = json.loads(resp.content)
    else:
        print( resp.content )
        return False

    # Check that data exists and save it
    if 'name' in content and 'secretId' in content:
        if content['name'] != '' and content['secretId'] != '':
            with open('client_info.json', 'w') as outfile:
                json.dump(content, outfile)
                print( 'Device info save success' )
            return True
    print( 'Device info save unsuccessful' )
    return False
