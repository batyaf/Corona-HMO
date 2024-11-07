import pyodbc
from dto.corona_patient import  Corona_patient
import  validations as valid
from store import patient_store as ps

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')



def insert_corona_patient(new_cp):
    if up_corona_patient.PositivityDate == None:
        raise ValueError("missing Positivity Date")

    if not valid.date_greater(up_corona_patient.PositivityDate, up_corona_patient.recoveryDate):
        raise ValueError("Invalid  dates  recovery Date must be after Positivity Date")

    if not valid.validate_date(up_corona_patient.PositivityDate) or not valid.validate_date(
            up_corona_patient.recoveryDate):
        raise ValueError("Invalid date , cant be future date")
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        is_id=ps.get_Patient_by_id(new_cp.coronaPatientId)
        if is_id:
            query = f"INSERT INTO coronapatient VALUES (?, ?, ?)  coronaPatientId='{new_cp.coronaPatientId}'"
            cursor.execute(query, (new_cp.coronaPatientId, new_cp.PositivityDate, new_cp.recoveryDate))
            if cursor.rowcount <= 0:
                 raise ValueError("corona Patient insertion failed.")
        else:
            raise ValueError("Patient does not exist")


def update_corona_patient(up_corona_patient):

    if up_corona_patient.PositivityDate==None:
        raise ValueError("missing Positivity Date")

    if not valid.date_greater(up_corona_patient.PositivityDate,up_corona_patient.recoveryDate):
        raise ValueError("Invalid  dates  recovery Date must be after Positivity Date")

    if not valid.validate_date(up_corona_patient.PositivityDate) or not valid.validate_date(up_corona_patient.recoveryDate) :
        raise ValueError("Invalid date , cant be future date")

    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"update coronaPatient set PositivityDate='{up_corona_patient.PositivityDate}',recoveryDate='{up_corona_patient.recoveryDate}'  where coronaPatientId={up_corona_patient.coronaPatientId}"
        cursor.execute(query)
        if cursor.rowcount <= 0:
            raise ValueError("corona Patient update failed.")



def delete_corona_patient_by_id(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM coronaPatient WHERE coronaPatientId='{id}'"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_corona_patient_by_id(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM coronaPatient where coronaPatientId='{id}'"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 c=Corona_patient(id,row.PositivityDate,row.recoveryDate)
                 return c
             else:
                 return row




def get_all_corona_patients():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM coronapatient"
        data=cursor.execute(query)
        corona_patients = []
        row = data.fetchone()
        while row:
            c=Corona_patient(id,row.PositivityDate,row.recoveryDate)
            corona_patients.append(c)
            row = data.fetchone()
        return corona_patients





