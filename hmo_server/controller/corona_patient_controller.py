import json
from flask import Flask, jsonify, request
from store import corona_patient_store as cps
from dto.corona_patient import Corona_patient
from app import app


@app.route('/get_all_corona_patients', methods=['GET'])
def get_all_corona_patients():
    data=cps.get_all_corona_patients()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_vaccine_by_patient_id/<int:id>', methods=['GET'])
def get_vaccine_by_patient_id(id: int):
    data=cps.get_corona_patient_by_id(id)
    if data is not None:
         # return jsonify(data)
         return json.dumps(data.__dict__)
    else:
        return jsonify({'error': 'veccine not found'}), 404


@app.route('/insert_corona_patient', methods=['POST'])
def insert_corona_patient():
    new_cp = json.loads(request.data)
    new_cp =Corona_patient(**new_cp)
    is_inserted=cps.insert_corona_patient(new_cp)
    if(is_inserted==true):
        return jsonify({'message': 'corona patient inserted successfully'}), 200
    else:
        return jsonify({'error': 'corona patient not inserted'}), 404


@app.route('/update_corona_patient', methods=['PUT'])
def update_corona_patient():
    ud_cp = json.loads(request.data)
    ud_cp = Corona_patient(**ud_cp)
    isupdate=cps.update_corona_patient(ud_cp)
    if (isupdate):
        return jsonify({'message': 'corona patient delete successfully'}), 200
    else:
        return jsonify({'error': 'corona patient not update'}), 404

@app.route('/delete_corona_patient_by_id/<int:id>', methods=['DELETE'])
def delete_corona_patient_by_id(id: int):
    isdelete=cps.delete_corona_patient_by_id(id)
    if(isdelete):
        return jsonify({'message': 'corona patient delete successfully'}), 200
    else:
        return jsonify({'error': 'corona patient not delete'}), 404


