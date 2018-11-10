from ard_comms import getDistance, tally
from web_comms import postData, register

# Options
name = 'Mog'                                # Device name
secretId = 'dkw21ssdXa'                     # Secret id used to identify device
commands = ['tally', 'distance']            # Commands for this device

# Variables
command = ''
data = 0

def registration():
    res = register( commands )
    if res == True:
        return 'Registration successful'
    return 'Could not register to the web'

def mainLoop():

    command = 'distance'
    if command == 'distance':
        data = getDistance()
        postData( 'distance', data )

    #getCommand( name, secretId, url )

    #if command == 'tally':
    #    data = tally()
    #elif command == 'distance':
    #    data = getDistance()
    #    postData( name, secretId, command, data, urlSend )
