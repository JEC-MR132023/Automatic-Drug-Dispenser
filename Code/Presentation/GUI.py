import cv2
import tkinter as tk
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import sqlite3
import serial
import time

class QRCodeScannerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Medicine Dispenser")
        self.window.geometry("800x480")  # Set window size
        self.window.attributes("-fullscreen", True)  # Set window to full screen

        # Create a canvas for the background image
        self.canvas = tk.Canvas(window, width=800, height=480, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill and expand canvas to fill window

        # Load and display the background image
        self.bg_image = Image.open("bg.png")
        self.bg_image = self.bg_image.resize((800, 480), Image.LANCZOS)  # Resize with anti-aliasing
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        # Display welcome message

        # Create a button to start scanning QR codes
        self.scan_button = tk.Button(window, text="Scan QR Code", command=self.start_scanning, bg="blue", fg="white", font=("Arial", 12, "bold"))
        self.scan_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        # Initialize camera state
        self.cap = None
        self.camera_on = False

        # Connect to the SQLite database
        self.conn = sqlite3.connect('medicines.db')
        self.cur = self.conn.cursor()

        # Serial communication settings
        self.serial_port = '/dev/ttyUSB0'  # Change this to match your Arduino's serial port
        self.serial_baudrate = 9600  # Set baudrate to match Arduino's serial baudrate

        # Keep track of the welcome page window
        self.welcome_page_window = window

    def start_scanning(self):
        
        self.window.withdraw()
        
        # Hide welcome message and scan button
        self.scan_button.place_forget()

        # Start scanning QR codes
        self.toggle_camera()

    def toggle_camera(self):
        if not self.camera_on:
            # Open the video capture device (adjust the index if necessary)
            self.cap = cv2.VideoCapture(0)
            self.camera_on = True
            self.update_camera()  # Start updating the camera feed
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

                # Resize the image to fit the window
                img = img.resize((800, 480), Image.LANCZOS)

                # Convert the PIL Image to a Tkinter PhotoImage
                imgtk = ImageTk.PhotoImage(image=img)

                # Display the camera feed
                if hasattr(self, 'camera_label'):
                    self.camera_label.imgtk = imgtk
                    self.camera_label.config(image=imgtk)
                else:
                    self.camera_label = tk.Label(self.window, image=imgtk)
                    self.camera_label.image = imgtk  # Keep a reference to prevent garbage collection
                    self.camera_label.pack()

        # Call update_camera again after 10 milliseconds if camera is still on
        if self.camera_on:
            self.window.after(10, self.update_camera)


    def open_checkout_page(self, qr_data):
        # Close the main window
        self.window.withdraw()

        # Create a new window for checkout
        self.checkout_window = tk.Toplevel(self.window)
        self.checkout_window.title("Checkout")
        self.checkout_window.geometry("800x480")  # Set window size
        self.checkout_window.attributes("-fullscreen", True)  # Set window to full screen

        # Parse patient details from QR code data
        patient_details = self.get_patient_details(qr_data)

        # Display patient details
        patient_label = tk.Label(self.checkout_window, text=f"Patient ID: {patient_details['id']}\nName: {patient_details['name']}\nAge: {patient_details['age']}\nGender: {patient_details['gender']}")
        patient_label.pack(pady=10)

        # Display medicines for checkout
        medicines_frame = tk.Frame(self.checkout_window)
        medicines_frame.pack(pady=10)

        total_amount = 0

        self.quantity_entries = []
        self.prices = []  # Store prices of medicines
        self.ids = []  # Store IDs of medicines
        for medicine, quantity in patient_details['medicines'].items():
            medicine_info = f"{medicine}: {quantity}"
            medicine_label = tk.Label(medicines_frame, text=medicine_info)
            medicine_label.pack()

            # Entry for quantity
            quantity_frame = tk.Frame(medicines_frame)
            quantity_frame.pack()

            quantity_label = tk.Label(quantity_frame, text="Quantity:")
            quantity_label.pack(side=tk.LEFT)

            quantity_entry = tk.Entry(quantity_frame, width=5)
            quantity_entry.insert(0, str(quantity))
            quantity_entry.pack(side=tk.LEFT)

            # Check availability and collect price and ID
            availability, price, id = self.check_availability_and_price(medicine)
            price_label = tk.Label(quantity_frame, text=f"Price: ${price:.2f}")
            price_label.pack(side=tk.LEFT)

            self.quantity_entries.append(quantity_entry)
            self.prices.append(price)  # Store price for each medicine
            self.ids.append(id)  # Store ID for each medicine

            total_amount += quantity * price

        self.total_label = tk.Label(self.checkout_window, text=f"Total Amount: ${total_amount:.2f}", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)

        # Button to pay
        pay_button = tk.Button(self.checkout_window, text="Pay Now", command=self.pay_now, bg="green", fg="white", font=("Arial", 12, "bold"))
        pay_button.pack(pady=10)

    def get_patient_details(self, qr_data):
        # Parse patient details from QR code data
        patient_details = {}
        patient_details["name"], patient_details["age"], patient_details["gender"], patient_details["id"], medicines_str = qr_data.split(',')
        medicines = {}
        for item in medicines_str.split(';'):
            medicine, quantity = item.strip().split(':')
            medicines[medicine.strip()] = int(quantity.strip())
        patient_details["medicines"] = medicines
        return patient_details
    
    def check_availability_and_price(self, medicine):
        # Retrieve medicine details from the database
        self.cur.execute("SELECT stock, price, id FROM medicines WHERE name=?", (medicine,))
        result = self.cur.fetchone()
        if result:
            stock, price, id = result
            if stock > 0:
                return "Available", price, id
            else:
                return "Out of Stock", price, id
        else:
            return "Not Found", 0.0, None


    def pay_now(self):
        # Placeholder function for paying
        print("Payment processed successfully.")

        # Get IDs and quantities of selected medicines
        selected_medicines = [(self.ids[i], int(entry.get())) for i, entry in enumerate(self.quantity_entries) if self.ids[i] and int(entry.get()) > 0]

        # Open serial connection
        with serial.Serial(self.serial_port, self.serial_baudrate, timeout=1) as ser:
            # Send IDs serially based on their quantities
            for medicine_id, quantity in selected_medicines:
                for _ in range(quantity):
                    ser.write(str(medicine_id).encode())
                    ser.write(b'\n')  # Send newline character to signify end of message
                    print(f"Sent ID: {medicine_id}")

                    # Decrease quantity of medicine in the database
                    self.cur.execute("UPDATE medicines SET stock = stock - 1 WHERE id = ?", (medicine_id,))
                    self.conn.commit()

                    print(f"Quantity of medicine with ID {medicine_id} decreased by 1.")

        # Delay for 3 seconds
        time.sleep(3)

        # Close the checkout window
        self.checkout_window.destroy()

        # Display thank you page
        self.show_thank_you_page()

    def show_thank_you_page(self):
        # Hide the main page
        self.window.withdraw()

        # Create a new Tkinter window for the thank you page
        self.thank_you_window = tk.Toplevel(self.window)
        self.thank_you_window.title("Thank You")
        self.thank_you_window.geometry("800x480")  # Set window size
        self.thank_you_window.attributes("-fullscreen", True)  # Set window to full screen

        # Create and display the thank you message
        thank_you_label = tk.Label(self.thank_you_window, text="Thank you for using Automatic Medicine Dispenser", font=("Arial", 24))
        thank_you_label.pack(pady=50)

        # After 5 seconds, close the thank you page and show the welcome page again
        self.thank_you_window.after(5000, self.close_thank_you_page)

    def close_thank_you_page(self):
        # Close the thank you page
        self.thank_you_window.destroy()

        # Show the welcome page again
        self.welcome_page_window.deiconify()  # Show the main window again

        # Reset the camera feed
        self.toggle_camera()

# Create the Tkinter window
root = tk.Tk()

# Create the QRCodeScannerApp instance
app = QRCodeScannerApp(root)

# Run the Tkinter event loop
root.mainloop()
