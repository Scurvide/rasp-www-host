import serial, time

# Settings
usbDevice   = '/dev/ttyACM0'
serialPort  = 9600
timeoutIn   = 5    # Seconds
msgDistance = '7'   # Message for returning distance

# Variables
output = ''

# Open serial connection
ard = serial.Serial( usbDevice, serialPort, timeout = timeoutIn )
time.sleep( 1 )

# Returns sensor output or False if data collection failed
def getSensorData():

    # Send request to Arduino
    ard.write( msgDistance )

    # Read response from Arduino
    output = ''
    output = int(ard.readline())

    # Check if no data of value was received
    if output == 0 or output == '':
        print( 'Failed to receive data' )
        return False

    print( 'Distance: ' + str(output) + 'cm' )
    return output
