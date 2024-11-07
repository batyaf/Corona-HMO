import pyodbc
from dto.patient import  Patient
from dto.address import  Address
from dto.city import City
from store import corona_patient_store as cps
from store import vaccine_store as vs
from store import address_store as ads
from store import patient_image_store as pis
import json
import validations as valid

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')
               # 'Trusted_Connection=yes;')




def insert_patient(new_patient):
    if not all([new_patient.id, new_patient.firstName, new_patient.lastName, new_patient.dateOfBirth,
                new_patient.phone, new_patient.mobilePhone, new_patient.address]):
        raise ValueError("All mandatory fields must be provided.")

    if not valid.validate_phone(new_patient.phone) or not valid.validate_phone(new_patient.mobilePhone):
        raise ValueError("Invalid phone number format.")

    if not valid.validate_date(new_patient.dateOfBirth):
        raise ValueError("Invalid date of birth, cant be future date")

    if not valid.is_israeli_id(new_patient.id):
        raise ValueError("Invalid id number.")

    if not valid.contains_only_characters(new_patient.firstName) or not valid.contains_only_characters(new_patient.lastName):
        raise ValueError("Invalid name.")

    with pyodbc.connect(connect_str) as connection:
        with pyodbc.connect(connect_str) as connection:
            cursor = connection.cursor()
            new_patient.address.city=City(** new_patient.address.city)
            ads.insert_address(new_patient.address)
            query = f"select addressCode from address where street='{new_patient.address.street}' and houseNumber={new_patient.address.houseNumber} and cityCode={new_patient.address.city.cityCode}"
            data=cursor.execute(query)
            row = data.fetchone()
            address_code = row.addressCode
            id=get_Patient_by_id(new_patient.id)
            if id==None:
                query = "INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (new_patient.id, new_patient.firstName, new_patient.lastName,address_code,
                                       new_patient.dateOfBirth, new_patient.phone, new_patient.mobilePhone))
                if cursor.rowcount <= 0:
                    ads.delete_address_by_code(address_code)
                    raise ValueError("Patient insertion failed.")
            else:
                raise ValueError("Patient with the same ID already exists.")


def update_patient(patient):
    if not all([patient.id, patient.firstName, patient.lastName, patient.dateOfBirth,
                patient.phone, patient.mobilePhone, patient.address]):
        raise ValueError("All mandatory fields must be provided.")

    if not valid.validate_phone(patient.phone) or not valid.validate_phone(patient.mobilePhone):
        raise ValueError("Invalid phone number format.")

    if not valid.validate_date(patient.dateOfBirth):
        raise ValueError("Invalid date cant be future date")

    if not valid.contains_only_characters(patient.firstName) or not valid.contains_only_characters(patient.lastName):
        raise ValueError("Invalid name.")

    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        patient.address.city = City(**patient.address.city)
        ads.update_address(patient.address)
        id = get_Patient_by_id(patient.id)
        if id!=None:
            query = f"update Patient set firstName='{patient.firstName}',lastName='{patient.lastName}',dateOfBirth='{patient.dateOfBirth}',phone='{patient.phone}',mobilePhone='{patient.mobilePhone}'  where id='{patient.id}'"
            cursor.execute(query)
            if cursor.rowcount <= 0:
               raise ValueError("Patient updatat failed.")
        else:
            raise ValueError("Patient with the ID does not exists.")

def delete_Patient_by_id(id):
    delete_patient(id)
    ads.delete_address_by_code(row.addressCode)

def delete_patient(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             vs.get_all_vaccine_by_patient_id(id)
             cps.delete_corona_patient_by_id(id)
             query = f"select addressCode from patient where id='{id}'"
             cursor.execute(query)
             pis.delete_image_by_id(id)
             query = f"DELETE FROM Patient WHERE id='{id}'"
             cursor.execute(query)
             if cursor.rowcount <= 0:
                 raise ValueError("Patient deldete failed.")





def get_Patient_by_id(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM Patient p left join address a on p.addressCode=a.addressCode join city c on c.cityCode=a.cityCode   where id='{id}'"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 p = Patient(id=row.id,
                                   firstName=row.firstName,
                                   lastName=row.lastName,
                                   address=Address(
                                 addressCode=row.addressCode,
                                 city=City(cityCode=row.cityCode,cityName=row.cityName),
                                 street=row.street,
                                 houseNumber=row.houseNumber),
                                   dateOfBirth=row.dateOfBirth,
                                   phone=row.phone,
                                   mobilePhone=row.mobilePhone)
                 return p
             else:
                 return row




def get_all_Patient():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM Patient p left join address a on p.addressCode=a.addressCode join city c on c.cityCode=a.cityCode"
        data=cursor.execute(query)
        patients = []
        row = data.fetchone()
        while row:
            p = Patient(id=row.id,
                        firstName=row.firstName,
                        lastName=row.lastName,
                        address=Address(
                        addressCode=row.addressCode,
                        city=City(cityCode=row.cityCode, cityName=row.cityName),
                        street=row.street,
                        houseNumber=row.houseNumber),
                        dateOfBirth=row.dateOfBirth,
                        phone=row.phone,
                        mobilePhone=row.mobilePhone)
            patients.append(p)
            row = data.fetchone()
        return patients





def get_all_patient_corona_details(id):
    patient_data=get_Patient_by_id(id)
    corona_data=cps.get_corona_patient_by_id(id)
    vaccine_data=vs.get_all_vaccine_by_patient_id(id)
    patient_dict = {
        "id": patient_data.id,
        "firstName": patient_data.firstName,
        "lastName": patient_data.lastName,
        "dateOfBirth": patient_data.dateOfBirth,
        "phone": patient_data.phone,
        "mobilePhone": patient_data.mobilePhone,
        "address": {
            "street": patient_data.address.street,
            "addressCode": patient_data.address.addressCode,
            "houseNumber": patient_data.address.houseNumber,
            "city": {
                "cityName": patient_data.address.city.cityName,
                "cityCode": patient_data.address.city.cityCode
            }
        }
    }

    vaccine_list = []
    for v_data in vaccine_data:
        vaccine_json = {
            "vaccineCode": v_data.vaccineCode,
            "patientId": v_data.patientId,
            "dateOfVaccine": v_data.dateOfVaccine,
            "vaccineManufacturer": {
                "vaccineManufacturerCode": v_data.vaccineManufacturer.vaccineManufacturerCode,
                "manufacturerName": v_data.vaccineManufacturer.manufacturerName
            }
        }
        vaccine_list.append(vaccine_json)

    # Construct the patient_corona_data dictionary
    patient_corona_data = {
        "patient": patient_dict,
        "corona": corona_data.__dict__ if corona_data else {},
        "vaccines":vaccine_list
    }

    patient_corona_json = json.dumps(patient_corona_data)
    return patient_corona_json



