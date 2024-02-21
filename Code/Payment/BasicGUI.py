import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.selected = tk.BooleanVar(value=True)

class CombinedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Combined App")
        self.dark_mode = False
        self.running = True

        # Set the window size to 800x480 pixels
        self.root.geometry("800x480")

        # QR Code Scanner Initialization
        self.qr_code_frame = ttk.Frame(root)
        self.qr_code_frame.pack(padx=10, pady=10)
        self.create_qr_code_widgets()

        # Shopping Cart Initialization
        self.shopping_cart_frame = ttk.Frame(root)
        self.shopping_cart_frame.pack(padx=10, pady=10)
        self.shopping_cart_products = [
            Product("Paracetamol 500 mg", 75.00),
            Product("Shelcal 500", 120.00),
            Product("Vitamin E", 47.00),
        ]
        self.product_checkboxes = []
        self.create_shopping_cart_widgets()

        # Payment Page Initialization
        self.payment_frame = ttk.Frame(root)
        self.payment_frame.pack(padx=10, pady=10)
        self.create_payment_widgets()

        # Show the QR code scanner by default
        self.show_qr_code_scanner()

    def create_qr_code_widgets(self):
        welcome_label = tk.Label(self.qr_code_frame, text="Welcome to the Medical Dispenser", font=("Helvetica", 16))
        welcome_label.pack(pady=10)

        ttk.Separator(self.qr_code_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=10)

        video_label = tk.Label(self.qr_code_frame)
        video_label.pack()

        self.qr_code_thread = threading.Thread(target=self.start_video_feed, daemon=True)
        self.qr_code_thread.start()

        self.qr_code_detector = cv2.QRCodeDetector()

        assistance_button = tk.Button(self.qr_code_frame, text="Need Assistance?", command=self.request_assistance)
        assistance_button.pack(side=tk.RIGHT, padx=5, pady=5)

        input_qr_button = tk.Button(self.qr_code_frame, text="Scan QR", command=self.input_qr, font=("Helvetica", 14))
        input_qr_button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_shopping_cart_widgets(self):
        title_label = tk.Label(self.shopping_cart_frame, text="Automatic Medical Dispenser", font=("Helvetica", 20, "bold"), fg="#3498db")
        title_label.grid(row=0, column=0, columnspan=3, pady=15)

        heading_label = tk.Label(self.shopping_cart_frame, text="Order Page", font=("Helvetica", 16, "bold"), fg="#2ecc71")
        heading_label.grid(row=1, column=0, columnspan=3, pady=10)

        for i, product in enumerate(self.shopping_cart_products):
            name_label = tk.Label(self.shopping_cart_frame, text=f"{product.name}", font=("Helvetica", 12), fg="#34495e", anchor=tk.W)
            name_label.grid(row=i + 2, column=0, pady=5, padx=10, sticky="w")

            price_label = tk.Label(self.shopping_cart_frame, text=f"Rs {product.price:.2f}", font=("Helvetica", 12), fg="#34495e", anchor=tk.W)
            price_label.grid(row=i + 2, column=1, pady=5, padx=10, sticky="w")

            checkbox = tk.Checkbutton(self.shopping_cart_frame, text="", variable=product.selected, font=("Helvetica", 12), fg="#34495e", anchor=tk.E)
            checkbox.grid(row=i + 2, column=2, pady=5, padx=10, sticky="e")
            self.product_checkboxes.append(checkbox)

        # Checkout button on the shopping cart page
        checkout_button = tk.Button(self.shopping_cart_frame, text="Checkout", command=self.checkout, font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white", padx=20, pady=10)
        checkout_button.grid(row=len(self.shopping_cart_products) + 2, column=2, pady=20, sticky="e")

    def create_payment_widgets(self):
        payment_label = tk.Label(self.payment_frame, text="Payment Page", font=("Helvetica", 20, "bold"), fg="#3498db")
        payment_label.pack(pady=15)

        amount_label = tk.Label(self.payment_frame, text="Total Amount: Rs 0.00", font=("Helvetica", 16), fg="#34495e")
        amount_label.pack()

        # Add payment-related widgets here (Razorpay or other payment integration)

    def input_qr(self):
        # Action to be performed when the "Scan QR" button is clicked
        result = messagebox.askokcancel("Scan Prescription", "Scanning Your Prescription")
        if result:
            self.show_shopping_cart()

    def start_video_feed(self):
        capture = cv2.VideoCapture(0)

        while self.running:
            ret, frame = capture.read()

            if ret and self.running:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                decoded_objects, points, qr_code = self.qr_code_detector.detectAndDecodeMulti(rgb_frame)

                if len(decoded_objects) > 0:
                    for obj, pts in zip(decoded_objects, points):
                        rect_color = (0, 255, 0)
                        pts = pts.astype(int)
                        cv2.polylines(frame, [pts], isClosed=True, color=rect_color, thickness=2)

                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 0.5
                        font_color = (255, 255, 255)
                        font_thickness = 1
                        text_position = (pts[0, 0], pts[0, 1] - 10)
                        cv2.putText(frame, obj, text_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

                bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
                tk_image = ImageTk.PhotoImage(image=Image.fromarray(bgr_frame))

                video_label = tk.Label(self.qr_code_frame, image=tk_image)
                video_label.photo = tk_image
                video_label.pack()

                if len(decoded_objects) > 0:
                    self.show_qr_code_info(decoded_objects[0])

            self.qr_code_frame.update_idletasks()
            self.qr_code_frame.update()

        capture.release()

    def show_qr_code_info(self, qr_code_data):
        messagebox.showinfo("QR Code Scan", f"Scanned QR Code:\n{qr_code_data}")

    def request_assistance(self):
        messagebox.showinfo("Assistance", "Assistance is on the way!")

    def show_qr_code_scanner(self):
        self.shopping_cart_frame.pack_forget()
        self.payment_frame.pack_forget()
        self.qr_code_frame.pack()

    def show_shopping_cart(self):
        self.qr_code_frame.pack_forget()
        self.payment_frame.pack_forget()
        self.shopping_cart_frame.pack()

    def checkout(self):
        selected_products = [product.name for product in self.shopping_cart_products if product.selected.get()]

        if not selected_products:
            messagebox.showinfo("Checkout", "Please select at least one product.")
            return

        total_price = sum(product.price for product in self.shopping_cart_products if product.selected.get())
        messagebox.showinfo("Checkout", f"Selected Products: {', '.join(selected_products)}\nTotal Price: Rs {total_price:.2f}")

        # Show the payment page after checkout
        self.show_payment_page()

    def show_payment_page(self):
        self.shopping_cart_frame.pack_forget()
        self.qr_code_frame.pack_forget()
        self.payment_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedApp(root)
    root.mainloop()
