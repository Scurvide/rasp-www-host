import serial, time

# Settings
usbDevice       = '/dev/ttyACM0'
serialPort      = 9600
timeout         = 5     # Seconds
msgDistance     = '7'   # Message for returning distance
msgTally        = '3'   # Message for tally counting
msgResetTally   = '4' # Message for resetting tally counter

# Open serial connection
ard = serial.Serial( usbDevice, serialPort, timeout = timeout )
# Time needed for Arduino to reset and populate value array
time.sleep( 2 )

# Returns sensor output and unit or False if data collection failed
def getMeasurement( msg ):

    # Flush input buffer
    ard.reset_input_buffer()

    # Send request to Arduino
    ard.write( msg )
    # Read response from Arduino
    output = ''
    output = ard.readline()
    
    if output != '' and output != b'':
        # Measurement value and unit are separated by ';' in serial line
        # endline == '\r\n' which is removed with .splitlines()
        output = output.splitlines()
        serialData = output[0].split(';')

        if len( serialData ) == 1 or len( serialData ) == 2:
            try:
                value = float( serialData[0] )
            except ValueError:
                print( 'Could not turn number to float' )
                return False
            unit = ''
            if len( serialData ) == 2:
                unit = serialData[1]
            # Check if value received is more than 0
            if value > 0:
                print( 'Measured value: ' + str(value) + unit )
                return value, unit
            else:
                return False, ''
    print( 'Failed to receive measurement data' )
    return False, ''

# Returns True if something goes past
"""
def tally():

    # Send command to Arduino
    ard.write( msgTally )

    # Read response from Arduino if available
    output = ''
    buffer = ard.in_waiting
    if buffer == 3 or buffer == 6 or buffer == 9 or buffer == 12:
        output = ard.readline()
        if output != '' and output != b'':
            try:
                output = float(output)
            except ValueError:
                print( 'Arduino overflow buffer error. Continuing...' )
                return False
            if output == 1:
                print( 'Something went past' )
                return output
    elif buffer != 0:
        ard.reset_input_buffer()
        print( 'Serial input buffer reset' )
    return False
"""
