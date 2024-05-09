from flask import Flask, request, jsonify
import sqlite3
import hashlib
import secrets
import jwt

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('medicines.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()

# Secret key for JWT
SECRET_KEY = "123456"

# Helper function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password_hash = hash_password(data['password'])
    
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                       (username, password_hash))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        user_id, _, stored_password = user
        if hash_password(password) == stored_password:
            token = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid username or password'}), 401
@app.route('/meds', methods=['GET'])
def get_meds():
    cursor.execute('SELECT * FROM medicines')
    meds = cursor.fetchall()
    med_list = [{'id': med[0], 'name': med[1], 'dosage': med[2], 'price': med[3], 'stock': med[4]} for med in meds]
    return jsonify(med_list)

@app.route('/meds', methods=['POST'])
def add_med():
    data = request.json
    cursor.execute('INSERT INTO medicines (name, dosage, price, stock) VALUES (?, ?, ?, ?)',
                   (data['name'], data['dosage'], data['price'], data['stock']))
    conn.commit()
    return jsonify({'message': 'Medicine added successfully'}), 201

@app.route('/meds/<int:med_id>', methods=['PUT'])
def update_med(med_id):
    data = request.json
    cursor.execute('UPDATE medicines SET name=?, dosage=?, price=?, stock=? WHERE id=?',
                   (data['name'], data['dosage'], data['price'], data['stock'], med_id))
    conn.commit()
    return jsonify({'message': 'Medicine updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

