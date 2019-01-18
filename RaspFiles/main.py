from ard_comms import *
from web_comms import *
import time, threading, os

# Options
deleteDataOnBoot    = False       # Reset device to register again on boot
commands = [                      # Commands for this device
    'stop',
    'measurement',
    'tally'
    ]
# Client info storage location
clientInfoFile  = '/home/pi/DataCollection/RaspFiles/client_info.json'
commandRefreshTime  = 3           # (Seconds) Time interval for rechecking commands from online server
mainLoopInterval    = 1           # (Seconds) Time interval for mainLoop
sleepAfterDistance  = 1           # (Seconds) Sleep after distance measurement

# Variables
command = ''
data = 0
unit = ''
endProgram = False

def registration():
    res = register( clientInfoFile, commands )
    while res != True:
        if res == 'Reset':
            os.remove( clientInfoFile )
            print( 'Client info file deleted to request new Id on next try' )
            res = register( clientInfoFile, commands )
        else:
            return False
    return True

def getCommand():
    with open( clientInfoFile ) as client_info:
        file = json.load(client_info)
    return file[ 'command' ]

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

        command = getCommand()

        if command == 'measurement':
            data, unit = getMeasurement()
            if data != False:
                if not postData( clientInfoFile, data, unit ):
                    print( 'Data could not be saved' )
            print( '---------------------------------' )
            time.sleep( sleepAfterDistance )

        if command == 'tally':
            data = tally()
            if data != False:
                if not postData( clientInfoFile, data ):
                    print( 'Data could not be saved' )
                print( '---------------------------------' )
            else:
                print( 'Tally checked' )
                print( '---------------------------------' )

        time.sleep(mainLoopInterval)
    # Exceute mainLoop every mainLoopInterval seconds
    #threading.Timer(mainLoopInterval, mainLoop, [lastRefresh]).start()

def initialization():
    if deleteDataOnBoot == True:
        os.remove( clientInfoFile )
        print( ' ' )
        print( 'Client info deleted - deleteDataOnBoot option was True')
        print( '---------------------------------' )

    while registration() != True:
        print( 'Registration to the online server failed. Retrying...' )

    print( 'Connection established' )
    print( '---------------------------------' )
    mainLoop()

initialization()
