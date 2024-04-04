 //This is a test code for limit switch through the CNC shield
//The limit switch must be connected on the two terminals - NO and C

// Define the pin where the limit switch is connected on the CNC shield
#define LIMIT_SWITCH_PIN_X_MIN 9 
// 9 is the pin connected on X+/X- pin on the CNC Shield

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set the limit switch pin as input
  pinMode(LIMIT_SWITCH_PIN_X_MIN, INPUT_PULLUP); // Use INPUT_PULLUP to enable internal pull-up resistor
}

void loop() {
  // Read the state of the limit switch
  int limitSwitchState = digitalRead(LIMIT_SWITCH_PIN_X_MIN);

  // Print the state of the limit switch
  if (limitSwitchState == HIGH){
    Serial.println("Limit switch is not pressed");
  } else {
    Serial.println("Limit switch is pressed");
  }

  // Add a small delay to avoid rapid readings
  delay(100);
}
