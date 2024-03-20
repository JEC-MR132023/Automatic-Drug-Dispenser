#This code is to run a GUI app with QR code Scanner, Medicine Stack Number retrieval according to medicine name and quantity

import cv2
import tkinter as tk
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode

class QRCodeScannerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Medicine Dispenser")

        # Create a label for displaying the camera feed
        self.camera_label = tk.Label(window)
        self.camera_label.pack()

        # Create a label to display QR code data
        self.qr_label = tk.Label(window, text="", wraplength=300)
        self.qr_label.pack()

        # Create a button to start scanning QR codes
        self.scan_button = tk.Button(window, text="Scan QR Code", command=self.toggle_camera)
        self.scan_button.pack()

        # Initialize camera state
        self.cap = None
        self.camera_on = False

    def toggle_camera(self):
        if not self.camera_on:
            # Open the video capture device (adjust the index if necessary)
            self.cap = cv2.VideoCapture(1)
            self.camera_on = True
            self.update_camera()
        else:
            # Turn off the camera
            self.cap.release()
            self.camera_on = False

    def update_camera(self):
        if self.camera_on:
            # Read frame from the camera
            ret, frame = self.cap.read()

            if ret:
                # Convert the frame from BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to a PIL Image
                img = Image.fromarray(rgb_frame)

                # Convert the PIL Image to a Tkinter PhotoImage
                imgtk = ImageTk.PhotoImage(image=img)

                # Update the camera label with the new frame
                self.camera_label.imgtk = imgtk
                self.camera_label.config(image=imgtk)

                # Decode QR codes
                decoded_objects = decode(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

                # Process decoded objects
                for obj in decoded_objects:
                    # Print data of QR code
                    qr_data = obj.data.decode()
                    print("QR Code Data:", qr_data)

                    # Display QR code data
                    self.qr_label.config(text=qr_data)

                    # Parse patient details from QR code data
                    patient_details = self.get_patient_details(qr_data)

                    # Check medicine availability for the patient
                    available_stacks = self.check_medicine_availability(patient_details)
                    print("Available stack numbers:", available_stacks)

                    # Turn off the camera
                    self.cap.release()
                    self.camera_on = False

                    # Hide the camera display
                    self.camera_label.pack_forget()
                    break  # Exit the loop after processing the first QR code

                # Call update_camera again after 10 milliseconds
                self.window.after(10, self.update_camera)

    def get_patient_details(self, qr_data):
        # Parse patient details from QR code data
        # Assuming the QR code data is in the format 'name,age,gender,id,medicine1:quantity1;medicine2:quantity2;...'
        patient_details = {}
        patient_details["name"], patient_details["age"], patient_details["gender"], patient_details["id"], medicines_str = qr_data.split(',')
        medicines = {}
        for item in medicines_str.split(';'):
            medicine, quantity = item.strip().split(':')
            medicines[medicine.strip()] = int(quantity.strip())
        patient_details["medicines"] = medicines
        return patient_details

    def check_medicine_availability(self, patient_details):
        # Check medicine availability for the patient
        available_stacks = []
        medicines = patient_details.get("medicines", {})
        for medicine, quantity in medicines.items():
            if medicine in medicine_database:
                stack_number = medicine_database[medicine]["stack_number"]
                available_stacks.extend([str(stack_number)] * quantity)
        return ", ".join(available_stacks)

# Medicine database
medicine_database = {
    "Aspirin": {"stack_number": 1, "strips_per_stack": 10},
    "Paracetamol": {"stack_number": 2, "strips_per_stack": 8},
    "Ibuprofen": {"stack_number": 3, "strips_per_stack": 12},
    "Loratadine": {"stack_number": 4, "strips_per_stack": 6},
    "Amoxicillin": {"stack_number": 5, "strips_per_stack": 16},
    "Omeprazole": {"stack_number": 6, "strips_per_stack": 14},
    "Atorvastatin": {"stack_number": 7, "strips_per_stack": 10},
    "Simvastatin": {"stack_number": 8, "strips_per_stack": 10},
    "Metformin": {"stack_number": 9, "strips_per_stack": 12},
    "Losartan": {"stack_number": 10, "strips_per_stack": 8},
    "Amlodipine": {"stack_number": 11, "strips_per_stack": 10},
    "Albuterol": {"stack_number": 12, "strips_per_stack": 18},
    "Atenolol": {"stack_number": 13, "strips_per_stack": 10},
    "Tramadol": {"stack_number": 14, "strips_per_stack": 14},
    "Citalopram": {"stack_number": 15, "strips_per_stack": 12},
    "Gabapentin": {"stack_number": 16, "strips_per_stack": 8},
    "Duloxetine": {"stack_number": 17, "strips_per_stack": 10},
    "Warfarin": {"stack_number": 18, "strips_per_stack": 8},
    "Pregabalin": {"stack_number": 19, "strips_per_stack": 10},
    "Aripiprazole": {"stack_number": 20, "strips_per_stack": 6},
    "Risperidone": {"stack_number": 21, "strips_per_stack": 10},
    "Levothyroxine": {"stack_number": 22, "strips_per_stack": 8},
    "Phentermine": {"stack_number": 23, "strips_per_stack": 10},
    "Metoprolol": {"stack_number": 24, "strips_per_stack": 12}
}

# Create the Tkinter window
root = tk.Tk()

# Create the QRCodeScannerApp instance
app = QRCodeScannerApp(root)

# Run the Tkinter event loop
root.mainloop()
