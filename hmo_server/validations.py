import re
import datetime

def validate_phone(phone):
    pattern = re.compile(r'^([0]\d{1,3}[-])?\d{7,10}$')
    return bool(pattern.match(phone))

def validate_date(date):
    today = datetime.date.today()
    input_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    if input_date < today:
        return True
    else:
        return False
def date_greater(start,end):
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    return end>start

def is_israeli_id(id):
    return bool(re.fullmatch(r'\d{9}', id))

def contains_only_characters(input_string):
    return bool(re.match(r'^[a-zA-Z]+$', input_string))