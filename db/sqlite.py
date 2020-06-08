

import sqlite3 as sql
import os
from pprint import pprint as pp


def create_db(path_db, cities_filepath=os.getcwd()):
    """
        Процедура создаёт базу данных и 2 таблицы:
            1. Таблицу с отзывом - T_POSTS;
            2. Таблицу-справочник город-регион - RT_CITIES

        :param path_db: путь к базе данных (с именем бд)
        :param cities_filepath: путь к .csv файлу с городами (задан по умолчанию в текущей директории)
        
        :return -> None
    """

    conn = sql.connect(path_db)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE 'T_POSTS' 
        (
            id_post INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
            , first_name TEXT NOT NULL
            , last_name TEXT NOT NULL
            , patronomic TEXT NULL      
            , region TEXT NULL
            , city TEXT NULL
            , phone_number INTEGER NULL
            , email TEXT NULL
            , post TEXT NOT NULL
        );

        CREATE TABLE 'RT_CITIES'
        (
            city TEXT NOT NULL      -- Некоторые города в России имеют одинаковые названия
            , region TEXT NOT NULL 
        );
    """)

    cities_file = open(os.path.join(cities_filepath, "cities.csv"), 'r', encoding="utf-8")
    cities_list = []
    for line in cities_file:
        city, region = line.split(';')
        cities_list.append([city, region[:len(region)-1]])  # для region избавляемся от последнего символа '\n'
    cities_file.close()

    cursor.executemany("INSERT INTO 'RT_CITIES' ('city', 'region') VALUES (?, ?)", cities_list)
    conn.commit()
    conn.close()


def connect_to_db(path_db):
    """
        Создаёт соединение с базой данных 

        :param path_db: путь к базе данных с именем бд
        
        :return -> соединение или None
    """
    try:
        conn = sql.connect(path_db)
        return conn
    except sql.Error as error:
        print("DB Error: " + str(error))

    return None


def get_cities(conn, region):
    """
        Получение городов по выбранному региону

        :param conn: соединение с базой данных
        :param region: по какому региону селектить

        :return -> возвращаются все города из региона в виде списка
    """

    cursor = conn.cursor()

    query = """
        SELECT city
        FROM RT_CITIES
        WHERE region = ?;
        """

    cursor.execute(query, (region,))
    data = cursor.fetchall()    # получается список вида [('city_1',), ('city_2',), ('city_3',), ... ('city_n',)]
    return data


def get_regions(conn):
    """
        Получение всех регионов

        :param conn: соединение с базой данных

        :return -> возвращаются все регионы в виде списка
    """

    cursor = conn.cursor()

    query = """
        SELECT region
        FROM RT_CITIES
        GROUP BY region     -- чтобы выводились только уникальные регионы
        ORDER BY region;
        """

    cursor.execute(query)
    data = cursor.fetchall()    # получается список вида [('reg_1',), ('reg_2',), ('reg_3',), ... ('reg_n',)]
    return data


def get_stat_region(conn, reg="IS NOT NULL"):
    """
        Получение статистики по городу (возвращает кол-во комментариев по городу)

        :param conn: соединение с базой данных
        :param region: по какому региону селектить (по умолчанию выводит все регионы)

        :return -> кортеж (Регион, кол-во отзывов) или список кортежей
    """

    cursor = conn.cursor()

    # контроль изменения запроса
    check = lambda s: s if s == "IS NOT NULL" else str("= '{}'".format(s)) 
    
    query = """
        SELECT * 
        FROM 
        (
            SELECT 
                region
                , COUNT(post) as number_of_posts
            FROM
                T_POSTS
            WHERE 
                region {}
            GROUP BY
                region
        ) as T
        WHERE number_of_posts > 5
        ORDER BY
            T.number_of_posts
            , T.region;
        """.format(check(reg))

    cursor.execute(query)
    return cursor.fetchall()    # получается список вида [('reg_1', count), ..., ('reg_n', count)]


def get_stat_city(conn, reg="IS NOT NULL"):
    """
        Получение статистики по городам-регион (возвращает кол-во комментариев по городу)

        :param conn: соединение с базой данных
        :param reg: по какому региону селектить (по умолчанию выводит все города)

        :return -> кортеж (город, кол-во отзывов) или список кортежей
    """

    cursor = conn.cursor()

    # контроль изменения запроса
    check = lambda s: s if s == "IS NOT NULL" else str("= '{}'".format(s)) 
    
    query = """
        SELECT 
            city
            , COUNT(post) as number_of_posts
        FROM
            T_POSTS
        WHERE 
            region {}
        GROUP BY
            city
        ORDER BY
            COUNT(post)
            , city;
        """.format(check(reg))

    cursor.execute(query)
    return cursor.fetchall()    # получается список вида [('city_1', count), ..., ('city_n', count)]


def add_post(conn, first_name, last_name, post, patronomic="NULL"
            , region="NULL", city="NULL", phone_number="NULL", email="NULL"):
            """
                Добавление отзыва в таблицу

                :param conn: соединение с базой данных
                :остальные параметры говорят сами за себя

                :return -> None                
            """

            isNone = lambda value: "" if value is None else value # проверка на NoneType

            cursor = conn.cursor()

            query = """
                INSERT INTO T_POSTS (first_name, last_name, post, patronomic
                                    , region, city, phone_number, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """
            

            cursor.execute(query, [str(first_name), str(last_name), str(post), isNone(patronomic)
                                , isNone(region), isNone(city), isNone(phone_number), isNone(email), ])
            conn.commit()


def remove_post(conn, id_post):
    """
        Удаление выбранного поста

        :param conn: соединение с бд
        :param id_post: номер, удаляемого поста

        :return -> None
    """

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM T_POSTS
        WHERE id_post = ?;
    """, (id_post,))
    
    conn.commit()


def get_all_posts(conn):
    """
        Получение вcех комментариев

        :param conn: соединение с базой данных
        
        :return -> список кортежей (id_post, текст)
    """

    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_post, post
        FROM T_POSTS
        ORDER BY id_post;
    """)
    
    return cursor.fetchall()





def get_records(conn):
    """
    """

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *  FROM T_POSTS
    """)
    return cursor.fetchall()

def get_delete(conn):
    """
    """

    cursor = conn.cursor()

    cursor.execute("""
        Delete FROM T_POSTS
        where id = (?)
    """)
    return cursor.fetchall()




if __name__ == "__main__":  

    name_db = "feedback.db"
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, name_db)
    
    if not os.path.exists(path_db):
        try:
            create_db(path_db)
        except sql.Error as error:
            print("DB error: " + str(error))
    
    try:
        conn = connect_to_db(path_db)            

        # pp(get_cities(conn, "Краснодарский край"))
        # pp(get_stat_region(conn, "Краснодарский край"))
        # add_post(conn, "Игорь", "Масенко", "фыва", "Евгеньевич", "Краснодарский край", "Краснодар", "891833302090")
        # pp(get_stat_city(conn, "Краснодар"))
        # remove_post(conn, 3)
        # pp(get_regions(conn))
        # pp(get_all_posts(conn))

        pp(get_records(conn))
        conn.close()

    except sql.Error as error:
        print("DB error: " + str(error))

