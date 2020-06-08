#!/usr/bin/env python3
# coding: utf-8

# ВОЗРВРАЩАЕТ html-фрагмент ОТЗЫВОВ

import os
import sys
sys.path.insert(1, os.getcwd())
from db.sqlite import sql, create_db, connect_to_db, get_records
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
posts = get_records(conn)
conn.close()

print("Status: 200 OK")
print("Content-type: application/json\r\n\r\n")
print(JSONEncoder().encode(posts))