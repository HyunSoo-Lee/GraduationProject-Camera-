import db_connect as db

db.find_row('user', 'nickname', 'JHM')
id = db.find_id('user', 'nickname', 'JHM')
db.find_row('sleep_time', 'user_id', id)

