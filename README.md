# rasp-www-host
- Collects data from Arduino with Raspberry Pi and sends it to website for storage
- Collected data can be viewed publicly from the website
- Users can make some changes to the data collection operation via the website
- Website supports multiple Raspberry Pi data collectors at once

### Data Flowchart
[Image here]

## Table of Contents
- **Devices and Applications**
- **Installation**
- **Usage**
- **Credits**

## Devices and Applications
| Device/App | Model/Version | OS | Programming Language | Purpose |
| ------ | ------ | ------ | ------ | ------ |
| Raspberry Pi | 3 Model B+ | Raspbian Stretch Lite 4.14 | Python | Pass collected data to website. Receive commands from online server. |
| Arduino | Mega 2560 |  | C++ | Collect data from sensor and pass it to Raspberry Pi. |
| Ultrasonic Sensor | HC-SR04 |  |  | Gather data. |
| Django Framework | Django 2.1.5 |  | Python, Javascript | Web app hosted on HTTP online server. Receive and store data from Raspberry Pi. Allow users to view data publicly. Send instructions back to Raspberry Pi. |

## Installation
Linux bash is required to maintain and run this application. I use Ubuntu for Windows 10.

### Website Setup
#### Host the Website Locally
Raspberry Pi must be connected to the same local network for this to work easily.
I use Python 3.6.3 to run the website locally.  
Clone the repository to some folder your PC using git
```sh
$ git clone https://github.com/Scurvide/rasp-www-host.git
```
Install requirements with 
```sh
$ pip install -r requirements.txt
```
Check local ip address
```sh
$ ifconfig
```
Check value inet for local ip address, probably something like 192.168.X.X  
Add the ip address in RaspWWW/settings.py to allowed hosts
```sh
ALLOWED_HOSTS = [
  '192.168.X.X',
  'localhost',
]
```
Run the server with the local ip address and port 8000
```sh
$ python manage.py runserver 192.168.X.X:8000
```
Website should now be accessible by your browser at address 192.168.X.X:8000  

#### Or Host the Website on Heroku
Easy way to host the website is to connect Heroku app to a GitHub repository.  
Heroku is a free to use host to certain extent.
- Clone this repository for yourself and connect it to an app created in Heroku
- Keep requirements.txt up to date to any updates/changes done to plugins, languages, etc...
- If automatic deploys are set on in Heroku, any updates pushed to repository master branch update to the Heroku website automatically

### Raspberry Pi Setup
I use Raspbian Stretch Lite 4.14 as Operating System. Default Python 2.7.13 on Raspbian should be enough for this project. Raspberry Pi must be connected to the same local network as the website host. Or if website is hosted publicly, the Raspberry Pi must have connection to the internet.

#### Required Python modules
Install PySerial required for serial communication with Arduino.
Depending on the Python version you use, install either
```sh
$ sudo apt-get install python-serial
```
for python 2 or
```sh
$ sudo apt-get install python3-serial
```
for python 3 and above.  
Install Python requests required for communication with the website
```sh
$ sudo apt-get install python-requests
```

#### Website URL to RaspFiles/web_comms.py
Add website URL to variables urlSend and urlRegister
```sh
# Options
urlSend     = 'http://192.168.X.X:8000/send/'      # Url for sending data
urlRegister = 'http://192.168.X.X:8000/register/'  # Url for registering device
```

#### Client Info Storage Location and Collected Data Types to RaspFiles/main.py
Add path to where client info will be stored during operation.
```sh
# Client info storage location
clientInfoFile          = '/home/pi/RaspFiles/client_info.json'
```
Add collected data types settings as a dictionary to dataTypes list.  
```sh
dataTypes = [{                  # Data type definitions
    'dataType': 'distance',     # Datatype name
    'measureMsg': '7',          # Msg for requesting correct action from Arduino
    'graphType': 'point',       # Graph type that is shown online (point or bar)
    'measureRequests': True,    # Allow measuring requests from online (on user click)
    'autoMeasuring': True       # Allow auto measuring setting
    },
    { ... }]
```

#### Move RaspFiles to Raspberry Pi
Move RaspFiles folder to your Raspberry Pi user folder
```sh
/home/pi/RaspFiles'
```

#### Set Raspberry Pi to Start the App on Boot
A good guide for setting this up can be found here  
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/  
The program to start running the app is
```sh
/home/pi/RaspFiles/main.py'
```

### Arduino Setup
- Make changes to file ArduinoFiles/Distance_Sensing/Distance_Sensing.ino for desired operation
- Compile and load the code to Arduino with the Arduino application
- Connect Arduino to Raspberry Pi via USB

If you make any changes to these variables
```sh
const int serialPort    = 9600; // Serial port for communication
const int msgDistance   = '7';  // Message for returning current distance reading
const int msgTally      = '3';  // Message for returning 1 when something passes by
const int msgResetTally = '4';  // Message for resetting tally counter
```
Remember to make the same changes to RaspFiles/ard_comms.py serialPort and RaspFiles/main.py dataTypes list.

## Usage
The most important thing to configure is the Arduino to collect desired data and send it forward to Raspberry Pi based on the messages given. Raspberry Pi also needs the data type dictionary to dataTypes list in RaspFiles/main.py. The rest of the application should work as it is as long as the connections are correctly set up.  
**More in depth description on how each component functions can be found in comments on top of most files.**

### Run the App
If the app is not set to start itself on boot, navigate to RaspFiles folder on Raspberry Pi and start the application with
```sh
python main.py
```
If everything is configured correctly, the app should now register itself and start sending data to the website. Running the app manually prints any error messages to you that the app encounters.

### Arduino
Arduino passively collects data. In this case the collected data is from an ultrasonic sensor which measures distance. The collected data is stored in Arduino until a correct message from Raspberry Pi via USB Serial is recieved. Once a message is recieved the Arduino will write back to the serial the data point corresponding the message recieved. In this case either latest distance measurement or tally count of things that passed by the sensor.  
Arduino recieves simple numbers to determine what data to write back to serial
```sh
const int msgDistance   = '7';  // Message for returning current distance reading
const int msgTally      = '3';  // Message for returning 1 when something passes by
const int msgResetTally = '4';  // Message for resetting tally counter
```
Arduino then writes a row to serial in format that is understood by the Raspberry Pi
```sh
Serial.print(cm);
Serial.print(";");
Serial.println(unit);
```
Which results in 'cm;unit\r\n' to serial. Cm and unit are variables of which unit is optional.  
If unit is left out, simply use
```sh
Serial.println(cm);
```
to write to serial. The serial line writing must end with 'Serial.println()'.

### Raspberry Pi
Raspberry Pi communicates with the Arduino via USB Serial and the website via HTTP protocol. When sending data or registering to the website the Raspberry Pi informs the website of measurements it can make and then recieves instructions from the website on how to operate the measuring. Instructions and client information are stored to file on Raspberry Pi and with it can continue it's operation even after rebooting. Based on the instructions the Raspberry Pi writes messages to Arduino and recieves data corresponding the message written via serial. Data is then passed to the website where it is stored. Raspberry Pi updates the instructions whenever it communicates with the website.  
Supported data collection types are written in following format to RaspFiles/main.py
```sh
dataTypes = [{                  # Data type definitions
    'dataType': 'distance',     # Datatype name
    'measureMsg': '7',          # Msg for requesting correct action from Arduino
    'graphType': 'point',       # Graph type that is shown online (point or bar)
    'measureRequests': True,    # Allow measuring requests from online (on user click)
    'autoMeasuring': True       # Allow auto measuring setting
    },
    { ... }]                    # Optional second dataType dictionary and so on
```

### Website
Website stores data recieved from connected clients (Raspberry Pi) and includes a timestamp when it was saved. It then can present the data in graphs that has the latest 20 data points shown (Can be changed). User can choose from commands on the website to alter the operation of the Raspberry Pi data collection in predefined manner. User chosen command options are first stored in the website database and then passed to client as response the next time the client takes contact with the website. The website has syntax check that returns messages to help troubleshooting wrong syntax in sent data packages. The website can also delete clients and its data from the database which results in client having to reregister itself with the website.  
Data point amount shown in graphs can be changed in Datamana/data_view.py
```sh
# Options
dataPointsShown = 20
```

## Credits

#### Creator
Jani Hietala

#### Libraries and frameworks used
| Library/Framwork | URL |
| ------ | ------ |
| PySerial | https://pythonhosted.org/pyserial/ |
| Requests | http://docs.python-requests.org/en/master/ |
| Django | https://www.djangoproject.com/ |
