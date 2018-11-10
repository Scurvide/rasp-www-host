#include <NewPing.h>
// NewPing definements
#define TRIGGER_PIN  12
#define ECHO_PIN     10
#define MAX_DISTANCE 200 // Maximum distance (in centimeters). Maximum sensor distance is rated at 400-500cm.
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

// Options
const int led           = 13;   // Led pin
const int serialPort    = 9600;
const int msgDistance   = '7';  // Message for returning current distance reading
const int msgTally      = '3';  // Message for returning 1 when something passed by
const int attempts      = 10;   // Reattempts if sonar value is 0
const int attemptDelay  = 50;   // Milliseconds. Min 29ms
const int sample        = 5;    // How many values will be used for tallying
const int tallyTrigger  = 20;   // Change distance change required for tally trigger (cm)

// Variables
int msg                 = 0;
unsigned int cm         = 0;
int x                   = 0;
int average             = 0;
int total               = 0;
int tally               = 0;
unsigned int values[ sample ];

void setup() {
  // Serial Port begin
  Serial.begin (serialPort);

  // Inputs and Outputs
  pinMode(led, OUTPUT);
}

void loop() {

  // Data collection routine
  x = 0;
  cm = 0;
  total = 0;
  tally = 0;
  while (cm <= 0 && attempts > x) {
    cm = sonar.ping_cm();
    x++;
    delay(attemptDelay);
  }
  if ( average - tallyTrigger > cm ) {
    tally = 1;
  }
  for (int i = 0; i < sample - 1; i++) {
    values[i] = values[i + 1];
    total = total + values[i];
  }
  values[ sample - 1 ] = cm;
  total = total + cm;
  average = round( total / sample );

  // Message checking and action
  if (Serial.available() > 0) {
    msg = Serial.read();
  }
  if (msg == msgDistance) {
    Serial.println(cm);
  }
  if (msg == msgTally && tally == 1) {
    Serial.println(1);
    digitalWrite(led, HIGH);
    delay(500);
    digitalWrite(led, LOW);
  }
  delay(50);
}

