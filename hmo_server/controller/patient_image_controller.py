import json
from flask import Flask, jsonify, request
from store import patient_image_store as pis
from dto.patient_image import Patient_image
from app import app


@app.route('/get_all_images', methods=['GET'])
def get_all_images():
    data=pis.get_all_images()
    return json.dumps(data, default = lambda x: x.__dict__)

@app.route('/get_image_by_id/<int:id>', methods=['GET'])
def get_image_by_id(id: int):
    data=pis.get_image_by_id(id)
    if data is not None:
         return data
         # return json.dumps(data.__dict__)
    else:
        return jsonify({'error': 'image  not found'}), 404


@app.route('/insert_image', methods=['POST'])
def insert_image():
    try:
        new_image_file = request.files['file']
        patient_id = request.form.get('id')
        if new_image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        image_bytes = new_image_file.read()
        new_image = Patient_image(patientId=patient_id, image=image_bytes)
        is_inserted = pis.insert_image(new_image)

        if is_inserted:
            return jsonify({'message': 'Image inserted successfully'}), 200
        else:
            return jsonify({'error': 'Image not inserted'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/update_image', methods=['PUT'])
def update_image():
    ud_image = json.loads(request.data)
    ud_image = Patient_image(**ud_image)
    isupdate=pis.update_image(ud_image)
    if (isupdate):
        return jsonify({'message': 'image update successfully'}), 200
    else:
        return jsonify({'error': 'image not update'}), 404

@app.route('/delete_image_by_id/<int:id>', methods=['DELETE'])
def delete_image_by_id(id: int):
    isdelete=pis.delete_image_by_id(id)
    if(isdelete):
        return jsonify({'message': 'image delete successfully'}), 200
    else:
        return jsonify({'error': 'image not delete'}), 404


