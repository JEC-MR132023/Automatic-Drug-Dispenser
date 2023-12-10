from flask import Flask, render_template, request, jsonify
import qrcode
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.get_json()
    prescription_data = data['prescriptionData']

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(prescription_data)
    qr.make(fit=True)

    # Save QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_path = "static/prescription_qr.png"
    img.save(qr_code_path)

    return jsonify({'qrCodePath': qr_code_path})

if __name__ == '__main__':
    app.run(debug=True)
