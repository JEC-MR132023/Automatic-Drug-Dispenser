//This code has the limit switch working, the mimit switch function is now inside the movetoCoordinate function
//When the coordinate is sent and the robot is moving to the position, triggerring the limit switch stops the motor and when a new coordinate is given it resumes its operation and continues its movement to the old coordinate

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
#define STEPS_PER_REV 200
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

void moveEndEffectorToCoordinate(Coordinate coord) {
  // Convert coordinate values to steps
  long targetXSteps = coord.x * STEPS_PER_MM;
  long targetYSteps = coord.y * STEPS_PER_MM;

  // Move the X-axis stepper motor to the target position
  stepperX.moveTo(targetXSteps);

  // Move the Y-axis stepper motors to the target position
  stepperY1.moveTo(targetYSteps);
  stepperY2.moveTo(targetYSteps);

  // Run both Y-axis motors until they reach the target position
  while (stepperX.distanceToGo() != 0 || stepperY1.distanceToGo() != 0 || stepperY2.distanceToGo() != 0) {
    // Check X-axis limit switch
    if (isXLimitReached()) {
      Serial.println("X End Stop is triggered");
      stepperX.stop(); // Stop X-axis stepper motor if limit switch is triggered
      break; // Exit the loop immediately
    }

    // Check Y-axis limit switch
  //  if (isYLimitReached()) {
  //    Serial.println("Y End Stop is triggered");
  //    stepperY1.stop(); // Stop Y-axis stepper motor 1 if limit switch is triggered
  //    stepperY2.stop(); // Stop Y-axis stepper motor 2 if limit switch is triggered
  //    break; // Exit the loop immediately
  //  }

    stepperX.run();
    stepperY1.run();
    stepperY2.run();
  }
}


// Function to check X-axis limit switch
bool isXLimitReached() {
  return digitalRead(X_LIMIT_PIN) == HIGH; // Assuming the limit switch is normally closed (NC)
}

// Function to check Y-axis limit switch
bool isYLimitReached() {
  return digitalRead(Y_LIMIT_PIN) == HIGH; // Assuming the limit switch is normally closed (NC)
}

// Function to convert stack number to coordinate
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
  stepperY1.setMaxSpeed(2000.0);
  stepperY2.setMaxSpeed(2000.0);
  stepperY1.setAcceleration(1000.0);
  stepperY2.setAcceleration(1000.0);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);

  // Set up X axis
  stepperX.setMaxSpeed(1000.0);
  stepperX.setAcceleration(500.0);

  // Set limit switch pins as input with pull-up resistors enabled
  pinMode(X_LIMIT_PIN, INPUT_PULLUP);
  pinMode(Y_LIMIT_PIN, INPUT_PULLUP);

  // Initialize Serial communication
  Serial.begin(9600);
}

void loop() {
 

  // Check Y-axis limit switch
  //if (isYLimitReached()) {
  //  Serial.println("Y End Stop is triggered");
  //  stepperY1.stop(); // Stop Y-axis stepper motor 1 if limit switch is triggered
  //  stepperY2.stop(); // Stop Y-axis stepper motor 2 if limit switch is triggered
  //}

  // If data is available to read from Serial
  if (Serial.available() > 0) {
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

      // Check if stack number is within the valid range (1 to 24)
      if (stackNumber >= 1 && stackNumber <= 28) {
        // Convert stack number to coordinate
        Coordinate targetCoord = stackNumberToCoordinate(stackNumber);

        // Move end effector to the specified coordinate
        moveEndEffectorToCoordinate(targetCoord);
      } else {
        Serial.println("Invalid stack number. Please enter a number between 1 and 24.");
      }
    } else if (inputChar >= 'a' && inputChar <= 'g') {
      // Convert character input to corresponding stack number
      Coordinate targetCoord = stackNumberToCoordinate(inputChar);

      // Move end effector to the specified coordinate
      moveEndEffectorToCoordinate(targetCoord);
    } else {
      Serial.println("Invalid input. Please enter a number between 1 and 28 or a and g.");
    }
  }
}
