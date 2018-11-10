import serial, time

# Settings
usbDevice   = '/dev/ttyACM0'
serialPort  = 9600
timeoutIn   = 3     # Seconds
msgDistance = '7'   # Message for returning distance
msgTally    = '3'   # Message for tally counting

# Variables
output = ''

# Open serial connection
ard = serial.Serial( usbDevice, serialPort, timeout = timeoutIn )
# Time needed for Arduino to reset and populate value array
time.sleep( 2 )

# Returns sensor output or False if data collection failed
def getDistance():

    # Send request to Arduino
    ard.write( msgDistance )

    # Read response from Arduino
    output = ''
    output = ard.readline()
    if output != '':
        output = int(output)
        # Check if no data of value was received
        if output > 0:
            output = float(output) / 100
            print( 'Distance: ' + str(output) + 'm' )
            return output

    print( 'Failed to receive data' )
    return False

# Returns True if something goes past
def tally():

    # Send command to Arduino
    ard.write( msgTally )

    output = ''
    count = 0
    while True:
        output = ard.readline()
        if output != '':
            output = int(output)
        if output == 1:
            count = count + output
            print( 'Things gone past: ' + str(count) )
    if output == 1:
        print( 'Something went past' )
        return True
    print( 'Nothing went by' )
    return False
