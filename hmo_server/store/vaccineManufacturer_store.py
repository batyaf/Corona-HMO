import pyodbc
from dto.vaccine_manufacturer import Vaccine_manufacturer

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')



def insert_vaccine_manufacturer(new_vm):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO vaccineManufacturer VALUES (?)"
        cursor.execute(query, (new_vm.manufacturerName))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def update_vaccine_manufacturer(vm):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        code = get_vaccine_manufacturer_by_code(vm.vaccineManufacturerCode)
        if code!=None:
            query = f"update vaccineManufacturer set manufacturerName='{vm.manufacturerName}' where vaccineManufacturerCode={vm.vaccineManufacturerCode}"
            cursor.execute(query)
        if cursor.rowcount > 0:
            return True
        else:
            return False



def delete_vaccine_manufacturer_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM vaccineManufacturer WHERE vaccineManufacturerCode={code}"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_vaccine_manufacturer_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM vaccineManufacturer where vaccineManufacturerCode={code}"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 v=Vaccine_manufacturer(row.vaccineManufacturerCode,row.manufacturerName)
                 return v
             else:
                 return row




def get_all_vaccine_manufacturer():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM vaccineManufacturer"
        data=cursor.execute(query)
        vaccine_manufacturers = []
        row = data.fetchone()
        while row:
            v = Vaccine_manufacturer(row.vaccineManufacturerCode, row.manufacturerName)
            vaccine_manufacturers.append(v)
            row = data.fetchone()
        return vaccine_manufacturers






