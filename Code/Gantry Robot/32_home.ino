#include <AccelStepper.h>

// Define stepper motor connections and steps per revolution
#define enPin 8
#define X_STEP_PIN 2
#define X_DIR_PIN 5
#define Y1_STEP_PIN 3
#define Y1_DIR_PIN 6
#define Y2_STEP_PIN 4
#define Y2_DIR_PIN 7
#define X_LIMIT_PIN 9 // X-axis limit switch
#define Y_LIMIT_PIN 10 // Y-axis limit switch

#define STEPS_PER_REV 200
#define STEPS_PER_MM 10 // Steps per millimeter, adjust according to your setup

#define valve 11
#define pump A3
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
#define STACK_WIDTH_MM 57
#define STACK_HEIGHT_MM 45
bool isXHomed = false;
bool isYHomed = false;

void homeXAxis(AccelStepper &stepper, int limitSwitchPin) {
  stepper.setSpeed(500); // Adjust speed as necessary
  stepper.setAcceleration(500); // Adjust acceleration as necessary
  stepper.moveTo(-1); // Move towards the limit switch

  while (!digitalRead(limitSwitchPin)) {
    stepper.run();
  }

  stepper.setCurrentPosition(0); // Set current position as 0
  stepper.stop(); // Stop the motor
}

void homeYAxis(AccelStepper &stepper1, AccelStepper &stepper2, int limitSwitchPin) {
  stepper1.setSpeed(500); // Adjust speed as necessary
  stepper1.setAcceleration(500); // Adjust acceleration as necessary
  stepper2.setSpeed(500); // Adjust speed as necessary
  stepper2.setAcceleration(500); // Adjust acceleration as necessary
  
  // Move both Y-axis motors simultaneously towards the limit switch
  stepper1.moveTo(-1);
  stepper2.moveTo(-1);

  while (!digitalRead(limitSwitchPin)) {
    stepper1.run();
    stepper2.run();
  }

  // Set current position as 0 for both Y-axis motors
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);

  // Stop both Y-axis motors
  stepper1.stop();
  stepper2.stop();
}

void home() {
  homeXAxis(stepperX, X_LIMIT_PIN);
  homeYAxis(stepperY1, stepperY2, Y_LIMIT_PIN);
  isXHomed = true;
  isYHomed = true;
  Serial.println("System is at home position.");
}

// Function to move end effector to a specific coordinate
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
  digitalWrite(valve,HIGH);
  delay(1000);
  digitalWrite(valve,LOW);
}

// Function to check Y-axis limit switch
bool isYLimitReached() {
  return digitalRead(Y_LIMIT_PIN) == HIGH;
}
 

// Function to convert stack number to coordinate
Coordinate stackNumberToCoordinate(int stackNumber) {
  // Calculate X and Y coordinates based on stack number
  int xCoord = (stackNumber - 1) % 4; // Adjusted for 4 positions along X-axis
  int yCoord = (stackNumber - 1) / 4; // Adjusted for 8 positions along Y-axis
  return {xCoord * STACK_WIDTH_MM, yCoord * STACK_HEIGHT_MM};
}

void setup() {
  // Set maximum speed and acceleration for Y axes
  stepperY1.setMaxSpeed(1000.0);
  stepperY2.setMaxSpeed(1000.0);
  stepperY1.setAcceleration(500.0);
  stepperY2.setAcceleration(500.0);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);

  pinMode(valve,OUTPUT);
  pinMode(pump,OUTPUT);

  digitalWrite(pump,LOW);
  digitalWrite(valve,LOW);
  
  // Set up X axis
  stepperX.setMaxSpeed(1000.0);
  stepperX.setAcceleration(500.0);

  // Initialize homing switches as input with pull-up resistors
  pinMode(X_LIMIT_PIN, INPUT_PULLUP);
  pinMode(Y_LIMIT_PIN, INPUT_PULLUP);

  
  // Initialize Serial communication
  Serial.begin(9600);
  
  // Home the system during initialization
  home();
}

void loop() {

  digitalWrite(pump,LOW);
  // Check if data is available to read from Serial
  if (Serial.available() > 0) {
    // Read the input string from Serial
    String input = Serial.readStringUntil('\n');
    
    // Check if the input command is for homing
    if (input == "h") {
      // Reset homing flags
      isXHomed = false;
      isYHomed = false;
      // Home the system
      home();
      // Optionally, you can send a message indicating that homing is complete
      Serial.println("System homed successfully.");
    } else {
      // Parse input as stack number
      int stackNumber = input.toInt();
      
      // Check if stack number is within the valid range (1 to 32)
      if (stackNumber >= 1 && stackNumber <= 32) {
        // Convert stack number to coordinate
        Coordinate targetCoord = stackNumberToCoordinate(stackNumber);
        Serial.println("Moving to stack number: " + String(stackNumber));
        // Move end effector to the specified coordinate
        moveEndEffectorToCoordinate(targetCoord);
      } else {
        Serial.println("Invalid input. Please enter a valid stack number or 'home' to home the system.");
      }
    }
  }
}
