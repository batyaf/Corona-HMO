import pyodbc
from dto.patient_image import Patient_image

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')



def insert_image(new_image):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO patientImage (patientId, image) VALUES (?, ?)"
        cursor.execute(query, (new_image.patientId, new_image.image))
        connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False


def update_image(up_image):
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        id = get_image_by_id(up_image.patientId)
        if id!=None:
            query = f"update patientImage set image='{up_image.image}' where patientId={up_image.patientId}"
            cursor.execute(query)
        if cursor.rowcount > 0:
            return True
        else:
            return False



def delete_image_by_id(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"DELETE FROM patientImage WHERE patientId={id}"
             cursor.execute(query)
             if cursor.rowcount > 0:
                 return True
             else:
                 return False


def get_image_by_id(id):
         with pyodbc.connect(connect_str) as connection:
             cursor = connection.cursor()
             query = f"SELECT * FROM patientImage where  patientId={id}"
             data=cursor.execute(query)
             row=data.fetchone()
             if row:
                 # return base64.b64encode(row.image).decode('utf-8')
                 return row.image
             else:
                 return row


def get_all_images():
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM patientImage"
        data = cursor.execute(query)
        images = []
        row = data.fetchone()
        while row:
            i = Patient_image(row.patientId, row.image)
            images.append(i)
            row = data.fetchone()
        return images







