// Include the necessary libraries
#include <Stepper.h>

// Define the pins for the relays
#define PUMP_PIN 11
#define VALVE_PIN A3

#define RELAY_OFF HIGH
#define RELAY_ON LOW

void setup() {
  // Set the relay pins as outputs
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(VALVE_PIN, OUTPUT);

  // Initialize both relays to be off
 

  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    // Read the incoming byte
    char command = Serial.read();

    // Act based on the received command
    switch (command) {
      case '1':
        digitalWrite(PUMP_PIN, RELAY_ON); // Turn on pump
        break;
      case '2':
        digitalWrite(PUMP_PIN, RELAY_OFF);  // Turn off pump
        break;
      case '3':
        digitalWrite(VALVE_PIN, RELAY_ON); // Turn on valve
        break;
      case '4':
        digitalWrite(VALVE_PIN, RELAY_OFF);  // Turn off valve
        break;
      default:
        break;
    }
  }
}
