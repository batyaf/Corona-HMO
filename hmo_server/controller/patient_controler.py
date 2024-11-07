import json
from flask import Flask, jsonify, request
from store import patient_store as ps
from dto.patient import Patient
from dto.address import Address
from app import app


@app.route('/get_all_Patient', methods=['GET'])
def get_all_Patient():
    data=ps.get_all_Patient()
    if data is not None:
         return json.dumps(data, default = lambda x: x.__dict__),200
    else:
         return jsonify({'error': 'An unexpected error occurred.'}), 500

@app.route('/get_patient_by_id/<int:id>', methods=['GET'])
def get_patient_by_id(id: int):
    data=ps.get_Patient_by_id(id)
    if data is not None:
        return json.dumps(data, default=lambda x: x.__dict__), 200
    else:
        return jsonify({'error': 'Patient not found'}), 404


@app.route('/insert_patient', methods=['POST'])
def insert_patient():
    try:
        patient_data = json.loads(request.data)
        patient_data["address"] = Address(**patient_data["address"])
        patient = Patient(**patient_data)
        ps.insert_patient(patient)
        return jsonify({'message': 'Patient inserted successfully'}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500



@app.route('/update_patient', methods=['PUT'])
def update_patient():
    try:
        ud_patient = json.loads(request.data)
        ud_patient["address"] = Address(**ud_patient["address"])
        ud_patient = Patient(**ud_patient)
        ps.update_patient(ud_patient)
        return jsonify({'message': 'Patient update successfully'}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500



@app.route('/delete_patient/<int:id>', methods=['DELETE'])
def delete_patient(id: int):
    try:
        ps.delete_Patient_by_id(id)
        return jsonify({'message': 'Patient delete successfully'}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route('/get_all_patient_corona_details/<int:id>', methods=['GET'])
def get_all_patient_corona_details(id):
    return ps.get_all_patient_corona_details(id)

#
# @app.route('/get_all_patient_with_images', methods=['GET'])
# def get_all_patient_with_images():
#     try:
#         patients_with_images = ps.get_all_patient_with_images()
#         return jsonify(patients_with_images), 200
#     except Exception as e:
#         return jsonify({"error": "An unexpected error occurred."}), 500

