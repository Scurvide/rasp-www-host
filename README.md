# rasp-www-host
- Collects data from Arduino with Raspberry Pi and sends it to website for storage
- Collected data can be viewed publicly from the website
- Users can make some changes to the data collection operation via the website
- Website supports multiple Raspberry Pi data collectors at once

### Data Flowchart
[Image here]

## Table of Contents
- Devices and applications
- Installation
- Usage
- Operation
- Credits

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
$ python manage.py runserver 192.168.X.X 8000
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
clientInfoFile          = '/home/<Username>/RaspFiles/client_info.json'
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
/home/<Username>/RaspFiles'
```

#### Set Raspberry Pi to Start the App on Boot


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
### Run the App
If the app is not set to start itself on boot, navigate to RaspFiles folder on Raspberry Pi and start the application with
```sh
python main.py
```
