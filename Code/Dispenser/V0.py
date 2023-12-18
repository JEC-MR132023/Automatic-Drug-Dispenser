import time
import RPi.GPIO as GPIO
from gpiozero import Button
import cv2

# Define GPIO pins for stepper motor control
DIR_X = 20  # Direction pin for X-axis
STEP_X = 21  # Step pin for X-axis

DIR_Y = 23  # Direction pin for Y-axis
STEP_Y = 24  # Step pin for Y-axis

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_X, GPIO.OUT)
GPIO.setup(STEP_X, GPIO.OUT)

GPIO.setup(DIR_Y, GPIO.OUT)
GPIO.setup(STEP_Y, GPIO.OUT)

# Set up GPIO for button
button = Button(17)

# Function to move the stepper motor for a specified number of steps
def move_stepper_motor(axis, direction, steps, delay):
    GPIO.output(axis['DIR'], direction)
    for _ in range(steps):
        GPIO.output(axis['STEP'], GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(axis['STEP'], GPIO.LOW)
        time.sleep(delay)

# Function to move the dispenser to a specified location
def move_dispenser(x, y):
    move_stepper_motor({'DIR': DIR_X, 'STEP': STEP_X}, GPIO.HIGH, x, 0.002)
    move_stepper_motor({'DIR': DIR_Y, 'STEP': STEP_Y}, GPIO.HIGH, y, 0.002)

# Function to control the vacuum-based end effector
def control_vacuum_system(command):
    # Placeholder code to control the vacuum system
    # You should replace this with the actual control logic for your vacuum system
    pass

# Function to dispense a medicine strip using the vacuum-based end effector
def dispense_medicine_vacuum(medicine_location):
    x_dispense, y_dispense = medicine_location['location']
    move_dispenser(x_dispense, y_dispense)
    control_vacuum_system("activate")  # Activate the vacuum system to pick up medicine
    time.sleep(1)  # Assume 1 second for picking up the medicine
    control_vacuum_system("deactivate")  # Deactivate the vacuum system
    # Code to dispense the medicine strip from the specified location
    print(f"Dispensing {medicine_location['name']} using vacuum")

# Function to retrieve prescription details from the database
def retrieve_prescription_details(qr_code_text):
    # Placeholder implementation
    # In a real system, you would parse the QR code text and query a database
    return {"name": "Medicine_A", "location": (10, 20)}

# Function to capture QR code using OpenCV
def capture_qr_code():
    # Placeholder implementation using OpenCV
    # Assumes you have OpenCV installed on your Raspberry Pi
    # You may need to adjust camera settings based on your setup
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cap.release()
    return frame

# Example: Scan QR code and dispense medicine
while True:
    button.wait_for_press()
    
    # Capture QR code image
    qr_code_image = capture_qr_code()

    # Assume qr_code_text is the scanned text from the QR code
    qr_code_text = "SampleQRCodeText"
    prescription_details = retrieve_prescription_details(qr_code_text)

    # Example: Dispense Medicine using the vacuum-based end effector
    dispense_medicine_vacuum(prescription_details)

    # Reset button state
    button.wait_for_release()

# Clean up GPIO on program exit
GPIO.cleanup()
