from base64 import b64encode
from flask import Flask, render_template, request, redirect, url_for, session
import qrcode
from PIL import Image
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ashishjoy'  # Change this to a secure secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'  # SQLite database file
db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['docUsername']
    email = request.form['docEmail']
    password = request.form['docPassword']

    with app.app_context():
        if Doctor.query.filter_by(username=username).first():
            return "Username already exists. Please choose another."

        new_doctor = Doctor(username=username, email=email, password=password)
        db.session.add(new_doctor)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['loginUsername']
    password = request.form['loginPassword']

    with app.app_context():
        doctor = Doctor.query.filter_by(username=username, password=password).first()

    if doctor:
        session['username'] = username
        return redirect(url_for('prescription'))

    else:
        return "Invalid username or password."

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    # Ensure the user is logged in before accessing the prescription page
    if 'username' not in session:
        return redirect(url_for('index'))

    # Initialize prescription_details and img_base64
    prescription_details = None
    img_base64 = None

    if request.method == 'POST':
        if 'submit_prescription' in request.form:
            # Process the prescription form data here
            patient_name = request.form.get('patientName')
            patient_id = request.form.get('patientId')
            age = request.form.get('age')
            gender = request.form.get('gender')
            weight = request.form.get('weight')

            # Medication details
            medicines = request.form.getlist('medicine[]')
            dosages = request.form.getlist('dosage[]')
            frequencies = request.form.getlist('frequency[]')
            durations = request.form.getlist('duration[]')

            # Build prescription details including patient information
            prescription_details = f"Patient Name: {patient_name}\nPatient ID: {patient_id}\nAge: {age}\nGender: {gender}\nWeight: {weight}\n"

            for med, dosage, freq, duration in zip(medicines, dosages, frequencies, durations):
                prescription_details += f"\nMedicine: {med}\nDosage: {dosage}\nFrequency: {freq}\nDuration: {duration}\n"

            # Print prescription details for debugging
            print("Prescription Details:")
            print(prescription_details)

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(prescription_details)
            qr.make(fit=True)

            # Create an in-memory image of the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = BytesIO()
            img.save(img_buffer)
            img_buffer.seek(0)

            # Convert image to base64 for displaying in HTML
            img_base64 = "data:image/png;base64," + b64encode(img_buffer.getvalue()).decode()

            # Store data in session
            session['prescription_details'] = prescription_details
            session['img_base64'] = img_base64

            # Redirect to prescription_with_qr
            return redirect(url_for('prescription_with_qr'))

    # Render the prescription form
    return render_template('prescription.html')

@app.route('/prescription_with_qr')
def prescription_with_qr():
    # Ensure the user is logged in before accessing the prescription_with_qr page
    if 'username' not in session:
        return redirect(url_for('index'))

    # Retrieve data from session
    prescription_details = session.get('prescription_details')
    img_base64 = session.get('img_base64')

    # Render the prescription_with_qr form
    return render_template('prescription_with_qr.html', prescription_details=prescription_details, img_base64=img_base64)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('prescription_details', None)
    session.pop('img_base64', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
