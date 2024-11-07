import json
from flask import Flask, jsonify, request
from store import city_store as cs
from dto.city import City
from app import app


@app.route('/get_all_cities', methods=['GET'])
def get_all_cities():
    data=cs.get_all_cities()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_city_by_code/<int:code>', methods=['GET'])
def get_city_by_code(code: int):
    data=cs.get_city_by_code(code)
    if data is not None:
         # return jsonify(data)
         return json.dumps(data.__dict__),200
    else:
        return jsonify({'error': 'city  not found'}), 404


@app.route('/insert_city', methods=['POST'])
def insert_city():
    new_c= json.loads(request.data)
    new_c = City(**new_c)
    is_inserted=cs.insert_city(new_c)
    if(is_inserted==True):
        return jsonify({'message': 'city  inserted successfully'}), 200
    else:
        return jsonify({'error': 'city  not insert'}), 404


@app.route('/update_city', methods=['PUT'])
def update_city():
    ud_city = json.loads(request.data)
    ud_city = City(**ud_city)
    isupdate=cs.update_city(ud_city)
    if (isupdate):
        return jsonify({'message': 'city  update successfully'}), 200
    else:
        return jsonify({'error': 'city  not update'}), 404

@app.route('/delete_city_by_code/<int:code>', methods=['DELETE'])
def delete_city_by_code(code: int):
    isdelete=cs.delete_city_by_code(code)
    if(isdelete):
        return jsonify({'message': 'city delete successfully'}), 200
    else:
        return jsonify({'error': 'city not delete'}), 404


