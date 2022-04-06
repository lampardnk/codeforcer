import requests
import json
from datetime import datetime
import pytz
import sys

import os
import mysql.connector

mysql_user = os.getenv("MYSQL_USER")
mysql_pwd = os.getenv("MYSQL_PWD")

mydb = mysql.connector.connect(
    host="localhost",
    user=f"{mysql_user}",
    password=f"{mysql_pwd}",
    database="codeforcer"
)

class Connect():
    def __enter__(self):
        cnx = mysql.connector.connect(
            host="localhost",
            port=3306,
            user=f"{mysql_user}",
            password=f"{mysql_pwd}",
            database="codeforcer"
        )
        self.cnx = cnx
        return cnx
    
    def __exit__(self, type, value, traceback):
        self.cnx.close()

testingServer = ['859772204812206080','951052594078433351']
logo = "https://bit.ly/cf-logo-dis"

emo = {
    'tick':"\U00002705",
    'x':"\U0000274E",
    'pistol':'\N{PISTOL}',
    'ok':'\N{OK HAND SIGN}',
    'cry':"\U0001F622"
}

def fetch(url):
    global c,e
    log_time = datetime.now(pytz.timezone('Asia/Singapore'))
    response = requests.get(url)

    try:
        if response.status_code == 200:
            c = response.content
            c = json.loads(c)
            e = False
        else:
            print(f"{log_time} CF API req returned {response.status_code}")
    except:
        e = True
        print(f"{log_time} Errors encountered")
        print(sys.exc_info())
        pass

    return c,e