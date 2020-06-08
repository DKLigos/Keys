#!/usr/bin/env python3



import cgi
import os
import sys
sys.path.insert(1, os.getcwd())
from db.sqlite import add_post, connect_to_db


def phone_to_int(phone_number):
    """
        Преобразование строкого номера телефона в целочисленный.
        Пример: из 8(xxx)-xx-xx-x в 7xxxxxxxx (только для Рос. номеров из 8 или +7 в 7)
            или из x-xxx-xxxxxx в xxxxxxxxx

        :param phone_number: входной номер телефона (str)

        :return -> номер телефона int
    """
    if not phone_number:
        return None

    result = ''
    for char in phone_number:
        if char.isdigit():
            result += char
    
    # преобразуем номер 8918... в 7918...
    if result[0] == '8':
        result = '7' + result[1:]

    return int(result)


form = cgi.FieldStorage()

first_name = form.getvalue("first_name")
second_name = form.getvalue("second_name")
post = form.getvalue("post")
patronomic = form.getvalue("patronomic")
city = form.getvalue("city")
reg = form.getvalue("reg")
phone = phone_to_int(form.getvalue("phone"))
email = form.getvalue("email")


name_db = "db/feedback.db"
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)



conn = connect_to_db(path_db)
add_post(conn, first_name, second_name, post, patronomic=patronomic
        , region=reg, city=city, phone_number=phone, email=email)
conn.close()

print("Status: 200 OK")
print("Content-type: text/html\r\n\r\n")

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Thank u!</title>
</head>
<style type="text/css">
    #container
    {
        display:inline-block;
        width: 350px;
        height: auto;
        position: relative;
        top: 13%;
        left: 40%;
    }
    h1, a
    {
        color: rgb(22, 29, 43);
        font-family: "Muller Light", 'Courier New', Courier, monospace;
    }
    h1 { font-size: 60pt; }
    a { font-size: 20pt; }
    #link {text-align: center; }
</style>
<body>
    <div id="container">
        <div id="thankfulness">
            <h1>Thank for feedback</h1>
        </div>
        <div id="link">
            <a href="http://localhost:8800/comment.html">Return</a>
        </div>
    </div>
</body>
</html>
""")
