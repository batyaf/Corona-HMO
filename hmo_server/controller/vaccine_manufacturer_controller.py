import json
from flask import Flask, jsonify, request
from store import vaccineManufacturer_store as vmf
from dto.vaccine_manufacturer import Vaccine_manufacturer
from app import app


@app.route('/get_all_vaccine_manufacturer', methods=['GET'])
def get_all_vaccine_manufacturer():
    data=vmf.get_all_vaccine_manufacturer()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_vaccine_manufacturer_by_code/<int:code>', methods=['GET'])
def get_vaccine_manufacturer_by_code(code: int):
    data=vmf.get_vaccine_manufacturer_by_code(code)
    if data is not None:
         # return jsonify(data)
         return json.dumps(data.__dict__)
    else:
        return jsonify({'error': 'vaccine manufacturer not found'}), 404


@app.route('/insert_vaccine_manufacturer', methods=['POST'])
def insert_vaccine_manufacturer():
    new_vmf= json.loads(request.data)
    new_vmf = Vaccine_manufacturer(**new_vmf)
    is_inserted=vmf.insert_vaccine_manufacturer(new_vmf)
    if(is_inserted==true):
        return jsonify({'message': 'vaccine manufacturer inserted successfully'}), 200
    else:
        return jsonify({'error': 'vaccine manufacturer not insert'}), 404


@app.route('/update_vaccine_manufacturer', methods=['PUT'])
def update_vaccine_manufacturer():
    ud_vaccinem = json.loads(request.data)
    ud_vaccinem = Vaccine_manufacturer(**ud_vaccinem)
    isupdate=vmf.update_vaccine_manufacturer(ud_vaccinem)
    if (isupdate):
        return jsonify({'message': 'vaccine manufacturer delete successfully'}), 200
    else:
        return jsonify({'error': 'vaccine manufacturer not delete'}), 404

@app.route('/delete_vaccine_manufacturer_by_code/<int:code>', methods=['DELETE'])
def delete_vaccine_manufacturer_by_code(code: int):
    isdelete=vmf.delete_vaccine_manufacturer_by_code(code)
    if(isdelete):
        return jsonify({'message': 'vaccine manufacturer delete successfully'}), 200
    else:
        return jsonify({'error': 'vaccine manufacturer not delete'}), 404


