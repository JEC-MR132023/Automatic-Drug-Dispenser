from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock data for testing
medicines = [
    {"id": 1, "name": "Aspirin", "dosage": "500mg", "price": 5.99},
    {"id": 2, "name": "Paracetamol", "dosage": "650mg", "price": 3.99},
    {"id": 3, "name": "Loratadine", "dosage": "10mg", "price": 7.99}
]

@app.route('/meds', methods=['GET'])
def get_meds():
    return jsonify(medicines)

@app.route('/meds/<int:med_id>', methods=['PUT'])
def update_med(med_id):
    med = next((med for med in medicines if med['id'] == med_id), None)
    if not med:
        return jsonify({'error': 'Medicine not found'}), 404
    data = request.json
    med['name'] = data.get('name', med['name'])
    med['dosage'] = data.get('dosage', med['dosage'])
    med['price'] = data.get('price', med['price'])
    return jsonify({'message': 'Medicine updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
