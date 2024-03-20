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
            self.cap = cv2.VideoCapture(0)
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

                    # Turn off the camera
                    self.cap.release()
                    self.camera_on = False

                    # Hide the camera display
                    self.camera_label.pack_forget()
                    break  # Exit the loop after processing the first QR code

                # Call update_camera again after 10 milliseconds
                self.window.after(10, self.update_camera)

# Create the Tkinter window
root = tk.Tk()

# Create the QRCodeScannerApp instance
app = QRCodeScannerApp(root)

# Run the Tkinter event loop
root.mainloop()
