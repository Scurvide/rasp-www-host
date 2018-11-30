import serial, time

# Settings
usbDevice   = '/dev/ttyACM0'
serialPort  = 9600
timeout     = 5     # Seconds
msgDistance = '7'   # Message for returning distance
msgTally    = '3'   # Message for tally counting

# Open serial connection
ard = serial.Serial( usbDevice, serialPort, timeout = timeout )
# Time needed for Arduino to reset and populate value array
time.sleep( 2 )

# Returns sensor output or False if data collection failed
def getDistance():

    # Flush input buffer
    ard.reset_input_buffer()

    # Send request to Arduino
    ard.write( msgDistance )
    # Read response from Arduino
    output = ''
    output = ard.readline()
    if output != '' and output != b'':
        output = float(output)
        # Check if no data of value was received
        if output > 0:
            output = output / 100
            unit = 'm'
            print( 'Distance: ' + str(output) + unit )
            return output, unit
    print( 'Failed to receive distance data' )
    return False, ''

# Returns True if something goes past
def tally():

    # Send command to Arduino
    ard.write( msgTally )

    # Read response from Arduino if available
    output = ''
    buffer = ard.in_waiting
    if buffer == 3 or buffer == 6 or buffer == 9 or buffer == 12:
        output = ard.readline()
        if output != '' and output != b'':
            output = int(output)
            if output == 1:
                print( 'Something went past' )
                return output
    else:
        if buffer != 0:
            ard.reset_input_buffer()
            print( 'Serial input buffer reset' )
    return False
