from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from controller.patient_controler import *
from controller.vaccine_controller import *
from controller.address_controller import *
from controller.vaccine_manufacturer_controller import *
from controller.corona_patient_controller import *
from controller.city_controller import *
from controller.patient_image_controller import *
import data_summary
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   app.run(port=5000)















