import serial
import time

# Open serial connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change port if necessary

try:
    while True:
        # Prompt user for stack number
        stack_number = input("Enter stack number (1-24): ")
        
        # Send stack number to Arduino
        ser.write(str(stack_number).encode() + b'\n')
        
        # Read response from Arduino
        response = ser.readline().decode('utf-8').strip()
        print("Arduino response:", response)
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
