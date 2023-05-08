import db_connect as db

#기본적인 row return
user_val = db.find_row('user', 'nickname', 'JHM')
print(user_val)
print("/////////////////")

#user id 가져오기
id = db.find_id('user', 'nickname', 'JHM')
print(id)
print("/////////////////")

#특정 값 바꾸기
sleep_val = db.find_row('sleep_time', 'user_id', id)
#new_value = sleep_val[3] + 1
new_value = 0
db.edit_val(id, 'sleep_time', 'turn_cnt', new_value)
new_sleep_val = db.find_row('sleep_time', 'user_id', id)
print(new_sleep_val)