import json
from flask import Flask, jsonify, request
from store import vaccine_store as vs
from dto.vaccine import Vaccine
from app import app


@app.route('/get_all_vaccine_by_patient_id/<int:id>', methods=['GET'])
def get_all_vaccine_by_patient_id(id: int):
    data=vs.get_all_vaccine_by_patient_id(id)
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_all_vaccine', methods=['GET'])
def get_all_vaccine():
    data=vs.get_all_vaccine()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_vaccine_by_code/<int:code>', methods=['GET'])
def get_vaccine_by_code(code: int):
    data=vs.get_vaccine_by_code(code)
    print(data)
    if data is not None:
         # return jsonify(data)
         return json.dumps(data.__dict__)
    else:
        return jsonify({'error': 'veccine not found'}), 404


@app.route('/insert_vaccine', methods=['POST'])
def insert_vaccine():
    vaccine = json.loads(request.data)
    vaccine =Vaccine(**vaccine)
    is_inserted=vs.insert_vaccine(vaccine)
    if(is_inserted==true):
        return jsonify({'message': 'vaccine inserted successfully'}), 200
    else:
        return jsonify({'error': 'there are 4 veccines'}), 404


@app.route('/update_vaccine', methods=['PUT'])
def update_vaccine():
    ud_vaccine = json.loads(request.data)
    ud_vaccine = Patient(**ud_vaccine)
    isupdate=vs.update_vaccine(ud_vaccine)
    if (isupdate):
        return jsonify({'message': 'vaccine delete successfully'}), 200
    else:
        return jsonify({'error': 'vaccine not delete'}), 404

@app.route('/delete_vaccine/<int:code>', methods=['DELETE'])
def delete_vaccine(code: int):
    isdelete=vs.delete_vaccine_by_code(code)
    if(isdelete):
        return jsonify({'message': 'vaccine delete successfully'}), 200
    else:
        return jsonify({'error': 'vaccine not delete'}), 404


