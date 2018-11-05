#include <NewPing.h>
// NewPing definements
#define TRIGGER_PIN  12
#define ECHO_PIN     10
#define MAX_DISTANCE 200 // Maximum distance (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

// Options
const int serialPort    = 9600;
const int msgDistance   = '7';  // Message for returning current distance reading
const int attempts      = 10;   // Reattempts if value is 0
const int attemptDelay  = 50;   // Milliseconds

// Variables
const int led           = 13;
int msg                 = 0;
unsigned int cm         = 0;
int x                   = 0;

void setup() {
  // Serial Port begin
  Serial.begin (serialPort);

  // Inputs and Outputs
  pinMode(led, OUTPUT);
}

void loop() {
  
  if (Serial.available() > 0) {
    msg = Serial.read();
    if (msg == msgDistance) {

        cm = 0;
        x = 0;
        while (cm <= 0 && attempts > x) {
          cm = sonar.ping_cm();
          x = x + 1;
          delay(50);
        }
        
        Serial.println(cm);

        // Blinks Led for <20cm to check that everything works
        if (cm < 20) {
          digitalWrite(led, HIGH);
          delay(250);
          digitalWrite(led, LOW);
        }
        else {
          delay(50);
        }
        
    }
  }
  else {
    delay(50);
  }
  
}
