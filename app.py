from flask import Flask, request, jsonify
from db import create_record, read_record, update_record, delete_record, search_records, load_database

app = Flask(__name__)

# Load the database at startup
load_database()

@app.route('/records', methods=['POST'])
def add_record():
    record = request.get_json()
    try:
        create_record(record)
        return jsonify({"message": "Record created successfully."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = read_record(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"error": "Record not found."}), 404

@app.route('/records/<int:record_id>', methods=['PUT'])
def update_existing_record(record_id):
    updated_record = request.get_json()
    try:
        print(record_id, updated_record)
        update_record(record_id, updated_record)
        return jsonify({"message": "Record updated successfully."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/records/<int:record_id>', methods=['DELETE'])
def delete_existing_record(record_id):
    delete_record(record_id)
    return jsonify({"message": "Record deleted successfully."}), 204

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = search_records(query)
    return jsonify(results), 200

if __name__ == '__main__':
    load_database()
    app.run(debug=True)
