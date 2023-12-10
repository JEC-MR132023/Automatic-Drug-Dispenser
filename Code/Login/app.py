from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in production
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
        return f"Welcome, {username}! You are now logged in."
    else:
        return "Invalid username or password."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
