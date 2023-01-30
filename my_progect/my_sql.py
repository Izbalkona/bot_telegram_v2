#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime

from my_settings import *

import pymysql
import pymysql.cursors

def verification_users(cursor, id_user): #верификацию пользователя в бд
    try:
        sql_request = (f"""
            SELECT id
            from MY_users
            where id_user = {id_user}""")

        cursor.execute(sql_request)
        result = cursor.fetchall()
        if result != (): # если запрос не пуст
            print(result[0]['id'])
        else:
            print("такого пользователя нет")
            #нужно занести в базу нового пользователя
            return ('create_user')
    except Exception as req_err:
        print('verification_users = ' + req_err)

def create_user(cursor, update):
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
                if verification_users(cursor, id_user) == 'create_user': #верификациz пользователя в бд
                    cursor.close()
                    with connection.cursor() as cursor: ## как обойтись 
                        create_user(cursor, update) #создадим нового пользователя если он не найден
                        connection.commit()
                print('done')
        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print('my_sqlbase = '+str(ex))

#https://habr.com/ru/post/321510/ понятная статья по sql