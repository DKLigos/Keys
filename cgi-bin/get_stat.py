#!/usr/bin/env python3
# coding: utf-8

# ВОЗРВРАЩАЕТ html-фрагмент СТАТИСТИКИ ПО РЕГИОНАМ

import os
import sys
sys.path.insert(1, os.getcwd())
from db.sqlite import sql, create_db, connect_to_db, get_stat_region, get_stat_city
from json import JSONEncoder

name_db = "db/feedback.db"
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)

if not os.path.exists(path_db):
    try:
        create_db(path_db, os.path.join(cur_dir, "db"))
    except sql.Error as error:
        print("DB Error: " + str(error))

conn = connect_to_db(path_db)
stat_reg = get_stat_region(conn)

stat_city = []
for reg, _ in stat_reg:
    stat_city.append((reg, get_stat_city(conn, reg)))    
    # получаем список вида [(reg, [(city1, count_city1), ..., (cityn, count_cityn)]), ...]


conn.close()

html = ''
print("Status: 200 OK")
print("Content-type: text/html\r\n\r\n")
print(JSONEncoder().encode(stat_city))


