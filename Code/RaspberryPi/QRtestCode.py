import cv2
from pyzbar.pyzbar import decode

def read_qr_code(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode QR codes
    decoded_objects = decode(gray)

    # Process decoded objects
    for obj in decoded_objects:
        # Print data of QR code
        print("QR Code Data:", obj.data.decode())

        # Draw bounding box around QR code
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw text with data
        cv2.putText(frame, obj.data.decode(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, decoded_objects

def main():
    # Open USB webcam
    cap = cv2.VideoCapture(0)

    # Flag to track if QR code has been detected
    qr_detected = False

    while cap.isOpened() and not qr_detected:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame to read QR code
        frame_with_qr, decoded_objects = read_qr_code(frame)

        # Display frame with QR code
        cv2.imshow('QR Code Scanner', frame_with_qr)

        # Check if QR code has been detected
        if decoded_objects:
            qr_detected = True

        # Check for 'q' key press to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Print the QR code data once
    if qr_detected:
        print("\nQR Code Data:", decoded_objects[0].data.decode())

if __name__ == '__main__':
    main()
