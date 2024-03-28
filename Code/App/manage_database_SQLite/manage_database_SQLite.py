from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('medicines.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')
conn.commit()

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
