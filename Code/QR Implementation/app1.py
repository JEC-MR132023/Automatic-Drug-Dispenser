from flask import Flask, render_template, request, jsonify
import qrcode
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    try:
        data = request.get_json()
        prescription_data = data['prescriptionData']

        # Extract patient name from prescription data
        patient_name = extract_patient_name(prescription_data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(prescription_data)
        qr.make(fit=True)

        # Save QR code image with patient's name as the filename
        qr_code_filename = f"static/{patient_name}_prescription_qr.png"
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_filename)

        return jsonify({'qrCodePath': qr_code_filename})

    except Exception as e:
        return jsonify({'error': str(e)})

def extract_patient_name(prescription_data):
    # Extract patient name from prescription data
    lines = prescription_data.split('\n')
    for line in lines:
        if line.startswith('Patient:'):
            return line.split(':', 1)[1].strip()

if __name__ == '__main__':
    app.run(debug=True)
