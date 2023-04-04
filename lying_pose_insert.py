import sys
import os
import pandas as pd
import base64
import requests
import pymysql as ps
from time import time
from time import localtime
from time import strftime

#db 정보 입력
dbname = 'graduation_db'
host = 'graduation-db.cicoecqa7q2u.ap-northeast-2.rds.amazonaws.com'
username = 'admin'
pw = 'sean9045'

#db 연결
conn = ps.connect(database = dbname, host = host, port = 3306, user = username, password = pw, charset = 'utf8')
cur = conn.cursor()
print(cur) #연결 성공 유무

import datetime
time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")  
print(time)
value = "'%s', '%s', '%s', '지짐이', '%s', 1" %('현수튀김', '1', '5000', time)

query = "INSERT into menu(menu_name, number, price, shop, startt, key_name) values(%s);" %(value)
print("Your Query is : %s" %query)
cur.execute(query)
conn.commit()

#연결 해제 (중요!)
conn.close()
