#!/usr/bin/env python3

import cgi
import os
import sys
sys.path.insert(1, os.getcwd())
from db.sqlite import connect_to_db, remove_post


name_db = "db/feedback.db"
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)


data = cgi.FieldStorage()
id_post = data.getvalue("param")
print(id_post)

conn = connect_to_db(path_db)
remove_post(conn, id_post)
conn.close()

print("Status: 200 OK")
print("Content-type: text/html\r\n\r\n")



