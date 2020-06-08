#!/usr/bin/env python3
# coding: utf-8

# ВОЗРВРАЩАЕТ html-фрагмент ГОРОДОВ ВЫБРАННОГО РЕГИОНА

import cgi
import os
import sys
from json import JSONEncoder 
sys.path.insert(1, os.getcwd())
from db.sqlite import sql, create_db, connect_to_db, get_cities


name_db = "db/feedback.db"
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)

if not os.path.exists(path_db):
    try:
        create_db(path_db, os.path.join(cur_dir, "db"))
    except sql.Error as error:
        print("DB Error: " + str(error))

form = cgi.FieldStorage()
if form.getvalue("reg"):
    reg = form.getvalue("reg")
else:
    reg = "none"

print("Status: 200 OK")
print("Content-type: application/json\r\n\r\n")


conn = connect_to_db(path_db)
cities = get_cities(conn, reg)
conn.close()

print(JSONEncoder().encode(cities))
