import pyodbc
from dto.vaccine import  Vaccine
from dto.vaccine_manufacturer import Vaccine_manufacturer

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')


def insert_vaccine(new_vaccine):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO vaccine VALUES (?, ?, ?) where 4 > (select count(*) from vaccine where patientId='{new_vaccine.patientId}')"
        cursor.execute(query, (new_vaccine.patientId,new_vaccine.dateOfVaccine,new_vaccine.vaccineManufacturerCode))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def update_vaccine(vaccine):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"update vaccine set patientId='{vaccine.patientId}',dateOfVaccine='{vaccine.dateOfVaccine}',vaccineManufacturerCode={vaccine.vaccineManufacturerCode}  where vaccineCode={vaccine.vaccineCode}"
        cursor.execute(query)
        if cursor.rowcount > 0:
            return True
        else:
            return False


def delete_vaccine_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM vaccine WHERE vaccineCode='{code}'"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_vaccine_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM vaccine v join vaccineManufacturer vm on v.vaccineManufacturerCode=vm.vaccineManufacturerCode  where vaccineCode='{code}'"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 v = Vaccine(vaccineCode=code,
                             patientId=row.patientId,
                             dateOfVaccine=row.dateOfVaccine,
                             vaccineManufacturer=Vaccine_manufacturer(vaccineManufacturerCode=row.vaccineManufacturerCode,manufacturerName=row.manufacturerName))
                 return v
             else:
                 return row




def get_all_vaccine():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM vaccine"
        data=cursor.execute(query)
        vaccines = []
        row = data.fetchone()
        while row:
            v = Vaccine(row.vaccineCode, row.patientId, row.dateOfVaccine, row.vaccineManufacturerCode)
            vaccines.append(v)
            row = data.fetchone()
        return vaccines

def get_all_vaccine_by_patient_id(patient_id):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM vaccine v join vaccineManufacturer vm on v.vaccineManufacturerCode=vm.vaccineManufacturerCode where patientId={patient_id}"
        data = cursor.execute(query)
        vaccines = []
        row = data.fetchone()
        while row:
            v = Vaccine(vaccineCode=row.vaccineCode,
                        patientId=row.patientId,
                        dateOfVaccine=row.dateOfVaccine,
                        vaccineManufacturer=Vaccine_manufacturer(vaccineManufacturerCode=row.vaccineManufacturerCode,
                                                                 manufacturerName=row.manufacturerName))
            vaccines.append(v)
            row = data.fetchone()
        return vaccines





