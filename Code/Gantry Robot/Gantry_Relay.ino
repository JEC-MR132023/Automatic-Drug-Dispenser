#include <AccelStepper.h>

// Define stepper motor connections and steps per revolution
#define enPin 8
#define X_STEP_PIN 2
#define X_DIR_PIN 5
#define Y1_STEP_PIN 3
#define Y1_DIR_PIN 6
#define Y2_STEP_PIN 4
#define Y2_DIR_PIN 7
#define X_LIMIT_PIN 9 // X-axis limit switch pin
#define Y_LIMIT_PIN 10 // Y-axis limit switch pin
#define RELAY_PIN 11 // Relay control pin
#define STEPS_PER_MM 10 // Steps per millimeter, adjust according to your setup

// Define stepper motor objects
AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY1(AccelStepper::DRIVER, Y1_STEP_PIN, Y1_DIR_PIN);
AccelStepper stepperY2(AccelStepper::DRIVER, Y2_STEP_PIN, Y2_DIR_PIN);

// Define a struct to hold coordinates
struct Coordinate {
  int x;
  int y;
};

// Define the size of each stack
#define STACK_WIDTH_MM 42 
#define STACK_HEIGHT_MM 55

// Define the coordinates for the 5th column
#define COLUMN_X_COORD 172 // X-coordinate for the 5th column

bool isXHomed = false;
bool isYHomed = false;

void homeAxis(AccelStepper &stepper, int limitSwitchPin) {
  stepper.setSpeed(100); // Adjust speed as necessary
  stepper.setAcceleration(100); // Adjust acceleration as necessary
  stepper.moveTo(-1); // Move towards the limit switch

  while (!digitalRead(limitSwitchPin)) {
    stepper.run();
  }

  stepper.setCurrentPosition(0); // Set current position as 0
  stepper.stop(); // Stop the motor
}

void home() {
  if (!isXHomed) {
    homeAxis(stepperX, X_LIMIT_PIN);
    isXHomed = true;
  }

  if (!isYHomed) {
    homeAxis(stepperY1, Y_LIMIT_PIN);
    homeAxis(stepperY2, Y_LIMIT_PIN);
    isYHomed = true;
  }
  
  // Check if both X and Y axes are homed
  if (isXHomed && isYHomed) {
    Serial.println("System is at home position.");
    // Optionally, you can set some flag or perform additional actions here
  }
}

void moveEndEffectorToCoordinate(Coordinate coord) {
  // Convert coordinate values to steps
  long targetXSteps = coord.x * STEPS_PER_MM;
  long targetYSteps = coord.y * STEPS_PER_MM;

  // Set maximum speed and acceleration for X axis
  stepperX.setMaxSpeed(2000);
  stepperX.setAcceleration(1000);

  // Set maximum speed and acceleration for Y axes
  stepperY1.setMaxSpeed(1000);
  stepperY2.setMaxSpeed(1000);
  stepperY1.setAcceleration(500);
  stepperY2.setAcceleration(500);

  // Move the X-axis stepper motor to the target position
  stepperX.moveTo(targetXSteps);

  // Move the Y-axis stepper motors to the target position
  stepperY1.moveTo(targetYSteps);
  stepperY2.moveTo(targetYSteps);

  // Run both Y-axis motors until they reach the target position
  while (stepperX.distanceToGo() != 0 || stepperY1.distanceToGo() != 0 || stepperY2.distanceToGo() != 0) {
    stepperX.run();
    stepperY1.run();
    stepperY2.run();
  }

  // Control relay based on the coordinate type
  
}


// Function to check Y-axis limit switch
bool isYLimitReached() {
  return digitalRead(Y_LIMIT_PIN) == HIGH;
}

// Function to convert stack number to coordinate
Coordinate stackNumberToCoordinate(int stackNumber) {
  if (stackNumber >= 1 && stackNumber <= 24) {
    // Calculate X and Y coordinates for regular stacks
    int xCoord = (stackNumber - 1) % 4; // Adjusted for 4 positions along X-axis
    int yCoord = (stackNumber - 1) / 4; // Adjusted for 6 positions along Y-axis
    return {xCoord * STACK_WIDTH_MM, yCoord * STACK_HEIGHT_MM};
  } else if (stackNumber >= 25 && stackNumber <= 28) {
    // Calculate coordinates for stacks 25 to 28 in the additional row
    int xCoord = (stackNumber - 25) % 4; // Adjusted for 4 positions along X-axis
    int yCoord = 6; // Y-coordinate for the additional row
    return {xCoord * STACK_WIDTH_MM, yCoord * STACK_HEIGHT_MM};
  } else {
    // Convert alphabets "a" to "g" to corresponding rows in the 5th column
    switch (stackNumber) {
      case 'a': return {COLUMN_X_COORD, 0};
      case 'b': return {COLUMN_X_COORD, 1 * STACK_HEIGHT_MM};
      case 'c': return {COLUMN_X_COORD, 2 * STACK_HEIGHT_MM};
      case 'd': return {COLUMN_X_COORD, 3 * STACK_HEIGHT_MM};
      case 'e': return {COLUMN_X_COORD, 4 * STACK_HEIGHT_MM};
      case 'f': return {COLUMN_X_COORD, 5 * STACK_HEIGHT_MM};
      case 'g': return {COLUMN_X_COORD, 6 * STACK_HEIGHT_MM}; // New row 'g'
      default: return {0, 0}; // Invalid input
    }
  }
}

void setup() {
  // Set maximum speed and acceleration for Y axes
  stepperY1.setMaxSpeed(4000.0);
  stepperY2.setMaxSpeed(4000.0);
  stepperY1.setAcceleration(2000.0);
  stepperY2.setAcceleration(2000.0);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);

  // Set up X axis
  stepperX.setMaxSpeed(2000.0);
  stepperX.setAcceleration(1000.0);

  // Set limit switch pins as input with pull-up resistors enabled
  pinMode(X_LIMIT_PIN, INPUT_PULLUP);
  pinMode(Y_LIMIT_PIN, INPUT_PULLUP);

  // Set relay pin as output
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Ensure relay is initially LOW

  // Initialize Serial communication
  Serial.begin(9600);

  // Home the system during initialization
  home();
}

void loop() {
  // If data is available to read from Serial
  if (Serial.available() > 0) {
    // Reset homing flags when new coordinates are given
    isXHomed = false;
    isYHomed = false;

    // Read the input string from Serial
    String input = Serial.readStringUntil('\n');

    // Parse input as stack number
    char inputChar = input.charAt(0);

    // Convert input to lowercase
    inputChar = tolower(inputChar);

    // Check if input is an integer or a character
    if (isdigit(inputChar)) {
      // Parse input as stack number
      int stackNumber = input.toInt();
      
      // Check if stack number is within the valid range (1 to 28)
      if (stackNumber >= 1 && stackNumber <= 28) {
        // Convert stack number to coordinate
        Coordinate targetCoord = stackNumberToCoordinate(stackNumber);
        Serial.println("The stack number is");
        Serial.print(stackNumber);
        // Move end effector to the specified coordinate
        moveEndEffectorToCoordinate(targetCoord);
        digitalWrite(RELAY_PIN, HIGH); // Engage relay if X coordinate is numeric
        Serial.println("Relay switched ON");
        
      } else {
        Serial.println("Invalid stack number. Please enter a number between 1 and 28.");
      }
    } else if (inputChar >= 'a' && inputChar <= 'g') {
      // Convert character input to corresponding stack number
      Coordinate targetCoord = stackNumberToCoordinate(inputChar);
      Serial.println("The stack number is");
      Serial.print(inputChar);
      // Move end effector to the specified coordinate
      moveEndEffectorToCoordinate(targetCoord);
      digitalWrite(RELAY_PIN, LOW); // Disengage relay if X coordinate is alphabetic
      Serial.println("Relay switched OFF");

    } else {
      Serial.println("Invalid input. Please enter a number between 1 and 28 or a and g.");
    }
  }
}
