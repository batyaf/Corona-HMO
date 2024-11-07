import pyodbc
from dto.address import  Address
from dto.city import City

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')



def insert_address(new_address):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO address VALUES (?,?, ?) "
        cursor.execute(query, (new_address.city.cityCode,new_address.street,new_address.houseNumber))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def update_address(address):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"update address set cityCode={address.city.cityCode},street='{address.street}',houseNumber={address.houseNumber} where addressCode={address.addressCode}"
        cursor.execute(query)
        if cursor.rowcount > 0:
            return True
        else:
            return False



def delete_address_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM address WHERE addressCode={code}"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_address_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM address where addressCode={code}"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 a=Address(addressCode=code,city=City(row.cityCode,row.cityName),street=row.street,houseNumber=row.houseNumber)
                 return a
             else:
                 return row




def get_all_adrdresses():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM address"
        data=cursor.execute(query)
        addresses = []
        row = data.fetchone()
        while row:
            a = Address(addressCode=code, city=City(row.cityCode, row.cityName), street=row.street,
                        houseNumber=row.houseNumber)
            addresses.append(a)
            row = data.fetchone()
        return patients






