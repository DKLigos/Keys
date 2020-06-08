#!/usr/bin/env python
# coding: utf-8

#""" ПОЛУЧЕНИЕ ВСЕХ РЕГИОНОВ ДЛЯ ВЫПАДАЮЩЕГО СПИСКА


import os
import sys
from json import JSONEncoder
sys.path.insert(1, os.getcwd())
from db.sqlite import sql, create_db, connect_to_db, get_regions

name_db = "db/feedback.db"
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)

if not os.path.exists(path_db):
    try:
        create_db(path_db, os.path.join(cur_dir, "db"))
    except sql.Error as error:
        print("DB Error: " + str(error))

conn = connect_to_db(path_db)
region = get_regions(conn)
conn.close()


print("Status: 200 OK")
print("Content-type: application/json\r\n\r\n")
print(JSONEncoder().encode(region))
