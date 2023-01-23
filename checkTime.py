from datetime import *
import json
import os
from os.path import exists

def checkNewDate():
    curr_date = datetime.now().date()

    with open('todayQuestion.json', 'r') as readFile:
        today = json.load(readFile)

    date = today["TODAY_DATE"]

    return curr_date != date

def check6AmPST():
    curr_time = datetime.utcnow()
    pst_6am = curr_time - timedelta(hours=8)
    return (pst_6am.hour == 6) and (pst_6am.min == 0)
