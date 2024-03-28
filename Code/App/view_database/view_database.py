from flask import Flask, jsonify

app = Flask(__name__)

# Mock data for testing
medicines = [
    {"name": "Aspirin", "dosage": "500mg"},
    {"name": "Paracetamol", "dosage": "650mg"},
    {"name": "Loratadine", "dosage": "10mg"}
]

@app.route('/meds', methods=['GET'])
def get_meds():
    return jsonify(medicines)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
