from ard_comms import *
from web_comms import *
import time, threading

# Options
name = 'Mog'                      # Desired device name (if available)
commands = [                      # Commands for this device
    'distance',
    'tally',
    'stop'
    ]
commandRefreshTime  = 5           # (Seconds) Time interval for rechecking commands from online server
mainLoopInterval    = 1           # (Seconds) Time interval for mainLoop
sleepAfterDistance  = 2           # (Seconds) Sleep after distance measurement

# Variables
command = ''
data = 0

def registration():
    res = register( commands, name )
    if res == True:
        return True
    return False

def getCommand():
    with open('client_info.json') as client_info:
        file = json.load(client_info)
    return file[ 'command' ]

def mainLoop( lastRefresh = time.time() ):

    # If time enough check command with web server
    if time.time() > lastRefresh + commandRefreshTime:
        print( 'Updating client info from server...' )
        if registration():
            lastRefresh = time.time()
        else:
            print( 'Command refresh failed' )
        print( '---------------------------------' )

    command = getCommand()

    if command == 'distance':
        data = getDistance()
        if data != False:
            if not postData( data ):
                print( 'Data could not be saved' )
        print( '---------------------------------' )
        time.sleep( sleepAfterDistance )

    if command == 'tally':
        data = tally()
        if data != False:
            if not postData( data ):
                print( 'Data could not be saved' )
            print( '---------------------------------' )
        else:
            print( 'Tally checked' )
            print( '---------------------------------' )

    # Exceute mainLoop every mainLoopInterval seconds
    threading.Timer(mainLoopInterval, mainLoop, [lastRefresh]).start()

def initialization():
    if registration():
        print( 'Connection established' )
        print( '---------------------------------' )
        mainLoop()
    else:
        print( 'Could not register with online server. Retrying in 5 seconds...' )
        print( '---------------------------------' )
        time.sleep( 5 )
        initialization()

initialization()
