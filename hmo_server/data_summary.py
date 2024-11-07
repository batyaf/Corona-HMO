import pyodbc
from datetime import datetime
import calendar
import json
from app import app

connect_str = ('DRIVER={SQL Server};'
               'SERVER=BATYA\SQLEXPRESS;'
               'DATABASE=Hmo')
today = datetime.today().date()
day_of_today = today.day

def get_all_days():
    today = datetime.now()
    month = today.month
    year = today.year
    days_list = [datetime(year, month, day).strftime('%d %b %Y') for day in range(1, day_of_today + 1)]
    return days_list


def amount_for_each_day():
    list = [0] * day_of_today
    with pyodbc.connect(connect_str) as connection:
        cursor = connection.cursor()
        query = """
      SELECT 
            CASE 
                WHEN DATEDIFF(DAY, [PositivityDate], DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)) >= 0 
                THEN DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
                ELSE [PositivityDate]
            END AS PositivityDate,
            CASE 
                WHEN DATEDIFF(DAY,[recoveryDate],GETDATE()) >= 0 
                THEN [recoveryDate]
                ELSE GETDATE()
            END AS recoveryDate
        FROM coronaPatient
        WHERE 
            DATEDIFF(DAY, [PositivityDate], GETDATE()) >= 0 
            AND (DATEDIFF(DAY, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1), [recoveryDate]) >= 0 OR [recoveryDate] IS NULL)
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            date_p = datetime.strptime(row.PositivityDate, '%Y-%m-%d')
            print(date_p)
            date_r = row.recoveryDate
            print(date_r)
            day_start = date_p.day
            day_end = date_r.day
            for d in range(day_start, day_end + 1):
                list[d - 1] += 1
        print(list)
        return list

def create_days_json(days,amount):
    jsonList = []
    for i in range(0, len(days)):
        jsonList.append({"day": days[i], "amount": amount[i]})
    return jsonList

@app.route('/get_data_summary', methods=['GET'])
def get_data_summary():
    day_list=get_all_days()
    amount_list=amount_for_each_day()
    data_json=create_days_json(day_list,amount_list)
    return  data_json