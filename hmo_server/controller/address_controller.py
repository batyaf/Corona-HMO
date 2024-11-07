import json
from flask import Flask, jsonify, request
from store import address_store as ads
from dto.address import Address
from app import app

@app.route('/get_all_adrdresses', methods=['GET'])
def get_all_adrdresses():
    data=ads.get_all_adrdresses()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_address_by_code/<int:code>', methods=['GET'])
def get_address_by_code(code: int):
    data=ads.get_address_by_code()
    if data is not None:
        address_data = {
            "street": data.address.street,
            "addressCode": data.address.addressCode,
            "houseNumber": data.address.houseNumber,
            "city": {
                "cityName": data.address.city.cityName,
                "cityCode": data.address.city.cityCode,
            }
        }
        return jsonify(address_data), 200
    else:
        return jsonify({'error': 'veccine not found'}), 404


@app.route('/insert_address', methods=['POST'])
def insert_address():
    address = json.loads(request.data)
    address =Address(**address)
    is_inserted=ads.insert_address(address)
    if(is_inserted==true):
        return jsonify({'message': 'vaccine inserted successfully'}), 200
    else:
        return jsonify({'error': 'there are 4 veccines'}), 404


@app.route('/update_address', methods=['PUT'])
def update_address():
    ud_address = json.loads(request.data)
    ud_address  = Address(**ud_address )
    is_update=ads.update_address(ud_address )
    if (is_update):
        return jsonify({'message': 'address update successfully'}), 200
    else:
        return jsonify({'error': 'address not update'}), 404


@app.route('/delete_address/<int:code>', methods=['DELETE'])
def delete_address(code: int):
    isdelete=ads.delete_address_by_code(code)
    if(isdelete):
        return jsonify({'message': 'address delete successfully'}), 200
    else:
        return jsonify({'error': 'address not delete'}), 404


