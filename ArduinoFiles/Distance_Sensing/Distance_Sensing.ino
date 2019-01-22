/*
Collects sensor data from HC-SR04 using NewPing library.
Reads serial port for instructions and sends data measurements
back to serial. Modes included are distance and tally.
Distance measures sensor distance from object in front of it.
Tally detects if something passes by the sensor.
*/

#include <NewPing.h>
// NewPing definements
#define TRIGGER_PIN  12  // Pin for trigger on Arduino board
#define ECHO_PIN     10  // Pin for echo on Arduino board
#define MAX_DISTANCE 200 // Maximum distance (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

// Options
const int led           = 13;   // Led pin
const int serialPort    = 9600; // Serial port for communication
const int msgDistance   = '7';  // Message for returning current distance reading
const int msgTally      = '3';  // Message for returning 1 when something passes by
const int msgResetTally = '4';  // Message for resetting tally counter
const int attempts      = 10;   // Reattempts if sonar returns value 0
const int attemptDelay  = 50;   // Milliseconds. Min 29ms
const int tallyTrigger  = 30;   // Change distance change required for tally trigger (cm)
const char unit[]       = "cm"; // Distance measurement unit

// Variables
int msg                 = 0;
int cm                  = 0;
int lastDistance        = 0;
int x                   = 0;
int tally               = 0;
int tallyCount          = 0;

void setup() {
    // Serial Port begin
    Serial.begin (serialPort);

    // Inputs and Outputs
    pinMode(led, OUTPUT);
}

void loop() {

    // Data collection routine
    x = 0;
    lastDistance = cm;
    cm = 0;
    tally = 0;
    while (cm <= 0 && attempts > x) {
        cm = sonar.ping_cm();
        x++;
        delay(attemptDelay);
    }
    if (lastDistance - cm > tallyTrigger) {
        tally = 1;
    }

    // Serial check for command
    if (Serial.available() > 0) {
        msg = Serial.read();

        // If command is distance, prints distance and unit to serial
        // Items in serial to be separated by ";"
        if (msg == msgDistance) {
            Serial.print(cm);
            Serial.print(";");
            Serial.println(unit);
            msg = 0;
        }
        // If command is tally, prints tallyCount to serial
        if (msg == msgTally) {
            Serial.println(tallyCount);
            tallyCount = 0;
            msg = 0;
        }

        // If command is clearTally, clears tallyCount
        if (msg == msgResetTally) {
            tallyCount = 0;
            Serial.println(tallyCount);
            msg = 0;
        }
    }

    // If tally triggers, adds +1 to tallyCount
    if (tally == 1) {
        if (tallyCount < 32700) {
          tallyCount++;
        }
        digitalWrite(led, HIGH);
        delay(500);
        digitalWrite(led, LOW);
    }

    delay(50);
}
