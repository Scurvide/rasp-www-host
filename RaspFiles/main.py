from ard_comms import *
from web_comms import *
import time, threading, os

# Options
dataTypes = [{                  # Data type definitions
    'dataType': 'distance',     # Datatype name
    'measureMsg': '7',          # Msg for requesting correct action from Arduino
    'graphType': 'point',       # Graph type that is shown online (point or bar)
    'measureRequests': True,    # Allow measuring requests from online (on user click)
    'autoMeasuring': True       # Allow auto measuring setting
    },{
    'dataType': 'tally',
    'measureMsg': '3',
    'graphType': 'bar',
    'measureRequests': False,
    'autoMeasuring': False
    }]
msgResetTally   = '4'   # Message for resetting tally counter
# Client info storage location
clientInfoFile          = '/home/pi/DataCollection/RaspFiles/client_info.json'
deleteDataOnBoot        = False         # Reset device to register again on boot
commandRefreshTime      = 0.5           # (Seconds) Time interval for rechecking commands from online server
mainLoopInterval        = 0.5           # (Seconds) Time interval for mainLoop
sleepAfterAutoMeasure   = 1.0           # (Seconds) Sleep after auto measurement

# Variables
commands = []
graphTypes = []
for type in dataTypes:                  # Build command type list for this device
    commands.append( type[ 'dataType' ] )
    graphTypes.append( type[ 'graphType' ] )
command = ''
data = 0
unit = ''
endProgram = False

def registration():
    res = register( clientInfoFile, commands, graphTypes )
    while res != True:
        if res == 'Reset':
            os.remove( clientInfoFile )
            print( 'Client info file deleted to request new Id on next try' )
            res = register( clientInfoFile, commands, graphTypes )
        else:
            return False
    return True

def getCommand():
    with open( clientInfoFile ) as client_info:
        file = json.load(client_info)
    return file[ 'command' ], file['measure'], file[ 'autoMeasure' ]

def mainLoop( lastRefresh = time.time() ):

    while endProgram == False:
        # If time enough check command with web server
        if time.time() > lastRefresh + commandRefreshTime:
            print( 'Updating client info from server...' )
            if registration():
                lastRefresh = time.time()
            else:
                print( 'Command refresh failed' )
            print( '---------------------------------' )

        command, requested, autoMeasure = getCommand()

        for type in dataTypes:
            if ( (command == type[ 'dataType' ] and type[ 'measureRequests' ] == False) or
                    (type[ 'measureRequests' ] == True and requested == True) or
                    (type[ 'autoMeasuring' ] == True and autoMeasure == True) ):

                data, unit = getMeasurement( type[ 'measureMsg' ] )
                if data != False:
                    if not postData( clientInfoFile, data, unit, type[ 'dataType' ] ):
                        print( 'Data could not be saved' )
                else:
                    print( 'Tally checked' )
                print( '---------------------------------' )

                if type[ 'autoMeasuring' ] == True and autoMeasure == True:
                    time.sleep( sleepAfterAutoMeasure )

        time.sleep(mainLoopInterval)
    # Exceute mainLoop every mainLoopInterval seconds
    #threading.Timer(mainLoopInterval, mainLoop, [lastRefresh]).start()

def measureAndPost( msg ):
    data, unit = getMeasurement( msg )

def initialization():
    print( ' ' )
    print( 'Initializing...' )
    if deleteDataOnBoot == True:
        os.remove( clientInfoFile )
        print( 'Client info deleted - deleteDataOnBoot option was True')
        print( '---------------------------------' )

    while registration() != True:
        print( 'Registration to the online server failed. Retrying...' )

    print( 'Connection established' )
    print( '---------------------------------' )
    mainLoop()

initialization()
