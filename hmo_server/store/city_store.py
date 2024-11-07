import pyodbc
from dto.city import City

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')



def insert_city(new_city):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO city VALUES (?)"
        cursor.execute(query, (new_city.cityName))
        if cursor.rowcount > 0:
            return True
        else:
            return False


def update_city(up_city):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        code = get_city_by_code(up_city.vaccineManufacturerCode)
        if code!=None:
            query = f"update city set cityName='{up_city.cityName}' where cityCode={up_city.cityCode}"
            cursor.execute(query)
        if cursor.rowcount > 0:
            return True
        else:
            return False



def delete_city_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM city WHERE cityCode={code}"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_city_by_code(code):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM city where  cityCode={code}"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 c=City(code,row.cityName)
                 return c
             else:
                 return row




def get_all_cities():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM city"
        data=cursor.execute(query)
        cities = []
        row = data.fetchone()
        while row:
            c = City(row.cityCode, row.cityName)
            cities.append(c)
            row = data.fetchone()
        return cities






