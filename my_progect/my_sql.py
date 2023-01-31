import datetime

from my_settings import *

import pymysql
import pymysql.cursors

def verification_users(cursor, id_user): #верификацию пользователя в бд
    try:
        sql_request = (f"""
            SELECT 
                id
            FROM 
                MY_users
            WHERE
                id_user = {id_user}""")

        cursor.execute(sql_request)
        result = cursor.fetchall()
        if result != (): # если запрос не пуст
            print("Пользователь найден")
        else:
            print("такого пользователя нет")
            #нужно занести в базу нового пользователя
            return ('create_user')
    except Exception as req_err:
        print('verification_users = ' + req_err)

def create_user(cursor, update): #создаем нового пользователя
    id_user = update.effective_chat.id
    user_name = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    time_registration = datetime.datetime.today().strftime("%Y-%m-%d  %H:%M:%S")

    try:
        cursor.execute(f"""
        INSERT INTO 
        MY_users (id_user)
        VALUES ({id_user}) ;""") #добавляем id нового пользователя чтобы определить его id в базе

        sql_request = (f"""
            SELECT id
            from MY_users
            where id_user = {id_user}""") # находим его id в базе 
            
        cursor.execute(sql_request)
        result = cursor.fetchall()
        print(result[0]['id'])

        cursor.execute(f"""
        INSERT INTO `users_table`(
        `id`, `user_name`, `first_name`, `last_name`,
        `date_of_registration`)
        VALUES(
        '{int(result[0]['id'])}', 
        '{user_name}', '{first_name}', '{last_name}',
        '{time_registration}'
        )""") #добавляем информацию о пользователе

        print("новый пользователь создан")
    except Exception as req_err:
        print("Connection refused...")
        print(str(req_err))

def add_daily_shopping_list(cursor, update): #добавить новый продукт в свой список
    id_user = update.effective_chat.id
    split_message = update.message.text.split()
    product_name = split_message[0]
    weight_count = split_message[1]
    period_day = split_message[2]
    try:
         cursor.execute(f"""
         INSERT INTO `daily_shopping_list`
            (`id`, `product_name`, `weight_count`, `period_day`) 
        VALUES 
            ('{id_user}','{product_name}','{weight_count}','{period_day}') """)

    except Exception as req_err:
        print("Connection refused...")
        print(str(req_err))

def show_daily_shopping_list(cursor, update, id_user): #показать таблицу пользователя
    id_user = update.effective_chat.id
    try:
        sql_request = (f"""
            SELECT
                `product_name`,
                `weight_count`,
                `period_day`
            FROM
                `daily_shopping_list`
            WHERE
                id = {id_user}""")

        cursor.execute(sql_request)
        result = cursor.fetchall()
        if result != (): # если запрос не пуст
            print("Таблица найдена")
            return result
        else:
            print("таблиц для такого пользователя нет")
            result("таблиц для такого пользователя нет")
            return result
    except Exception as req_err:
        print('verification_users = ' + req_err)

def remove_daily_shopping_list(cursor, update): #удалить продукт из своего списка
    split_message = update.message.text.split()
    product_name = split_message[1]
    print(product_name)
    try:
        print(product_name)
        cursor.execute(f"""
        DELETE FROM `daily_shopping_list` WHERE `product_name` = '{product_name}'
        """)
        print('Продукт успешно удален')
    except Exception as req_err:
        print("Connection refused...")
        print(str(req_err))

def clear_daily_shopping_list(cursor, update): #полностью очитстить свой список
    id_user = update.effective_chat.id
    try:
        cursor.execute(f"""
        DELETE FROM `daily_shopping_list` WHERE id = '{id_user}'
        """)
        print('Таблица успешно удалена')
    except Exception as req_err:
        print("Connection refused...")
        print(str(req_err))

def my_sqlbase(id_user, key, update, context): #сценарии взамодействия с базой проходят проверки
                               # 1) на подключение \
                               # 2) верификацию пользователя в бд)
    try: #пробуем подключиться к базе
        connection = pymysql.connect(host='localhost',
            user=my_user,
            password=my_password,
            db=my_db,
            port=my_port,
            cursorclass=pymysql.cursors.DictCursor)
        print('connect_succ')
        try:
            with connection.cursor() as cursor:
                if verification_users(cursor, id_user) == 'create_user': #верификация пользователя в бд
                    cursor.close()
                    with connection.cursor() as cursor: ## как обойтись 
                        create_user(cursor, update) #создадим нового пользователя если он не найден
                        connection.commit()
                if key == 'add_product':
                    add_daily_shopping_list(cursor, update)
                    connection.commit()
                elif key == 'show_my_table':
                    print('2sdfs')
                    result = show_daily_shopping_list(cursor, update, id_user)
                    connection.commit()
                    return result
                elif key == 'remove_product':
                    result = remove_daily_shopping_list(cursor, update)
                    connection.commit()
                    return result
                elif key == 'clear':
                    result = clear_daily_shopping_list(cursor, update)
                    connection.commit()
                    return result
        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print('my_sqlbase = '+str(ex))
