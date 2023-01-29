#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import logging


import pymysql
import pymysql.cursors


def check_sqlbase(user_name, user_password, user_var): #связь my_main с sql
    try:
        connection = pymysql.connect(host='localhost',
            user='root',
            password='root',
            db='test_bd',
            port=8889,
            cursorclass=pymysql.cursors.DictCursor)
        print('succ')
        try:
            with connection.cursor() as cursor:
                user_request_cell(cursor, user_name, user_password, user_var) #выводит любую информаци о пользователе по ключу user_name и соотвествию user_password
                #my_sql_insert(cursor, user_mail) #добавляет нового пользователя
        finally:
            connection.close()


    except Exception as ex:
        print("Connection refused...")
        print(ex)