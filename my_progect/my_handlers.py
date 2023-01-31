#!/usr/bin/python3
# -*- coding: utf-8 -*-
from my_sql import *

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler

from my_settings import *



markuup = ReplyKeyboardMarkup([['Мой список']], input_field_placeholder = 'dwad', resize_keyboard = True)

def start(update, context):
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text="""1. /day - укажите в какой день вы ходите за покупками\n
2. /show - показать список покупок, количество, период\n
3. чтобы добавить товар, просто напишите по форме\n
    название | кол-во | период в неделях\n
    пример:\n
    картошка 5кг 4\n
4. чтобы удалить продукт поставьте знак - название\n
    пример:\n
    - картошка\n
5. /clear полностью очистит вашу таблицу
6. есть возможность задать один из списков покупок на выбор
    /show_menu """ , parse_mode='html', reply_markup=markuup)

def show_menu(update, context):
    id_users = update.effective_chat.id
    context.bot.send_message( id_users,text="""
1. /show_sport - посмотреть товары
20.000 каллорий на неделю
2. /show_diet - посмотреть товары
14.000 каллорий на неделю""", parse_mode='html')



def clear(update, context): #удалить список покупок
    id_user = update.effective_chat.id
    key = 'clear'
    my_sqlbase(id_user, key, update, context) #key это ключ к сценарию

def show_sport(update, context):
    id_user = update.effective_chat.id
    menu = update.message.text
    dict_menu = {'/show_sport':'10'}
    id_menu = dict_menu[menu]
    key = 'show_my_table'
    print('id_menu =' + id_menu)
    result = select_mysql(id_menu, key, update, context)
    for product in result:
        text= f"""{product['product_name']} : {product['weight_count']} : {product['period_day']}"""
        print(text)
        context.bot.send_message( id_user, text=text ,  parse_mode='html' )


def select_mysql(update, context): #показать список покупок
    id_user = update.effective_chat.id
    key = 'show_my_table'
    result = my_sqlbase(id_user, key, update, context) #key это ключ к сценарию
    for product in result:
        text= f"""{product['product_name']} : {product['weight_count']} : {product['period_day']}"""
        print(text)
        context.bot.send_message( id_user, text=text ,  parse_mode='html' )
        
#тут идет обработка текста      
def echo(update, context) -> None: #регистрация любого сообщения, предлагаем каждую строчку добавить в таблицу, предварительно распарсив текст
    id_user = update.effective_chat.id
    logging.info(f'запрос пользователя {id_user} : {update.message.text}')
    split_message = update.message.text.split()
    if split_message[-1] == '?': #обработка знака вопроса в конце
        url = f'https://yandex.ru/images/search?from=tabbar&text=z%20yt%20jndtxf.%20yf%20djghjcs&p=9&pos=25&rpt=simage&img_url=http%3A%2F%2Fzvukobook.ru%2F800%2F600%2Fhttps%2Fotvet.imgsmail.ru%2Fdownload%2F251790489_2d40bec5d82c395f3c41de084db5ed56_800.jpg&lr=171920'
        context.bot.send_photo( id_user, url )
    elif update.message.text == "Мой список": #показать список покупок
        select_mysql(update, context)
    elif len(split_message) == 3: #добавляем продукт
        product_name = split_message[0]
        weight_count = split_message[1]
        period_day = split_message[2]

        text_split_message = f"""Товар успешно добавлен\n
        товар : <b>{product_name}</b>\n
        вес или кол-во : <b>{weight_count}</b>\n
        период : <b>{period_day}</b>"""
        context.bot.send_message( id_user, text=text_split_message,  parse_mode='html' )
        key = 'add_product'
        my_sqlbase( id_user, key, update, context )

    elif split_message[0] == '-': #удаляем продукт
        product_name = split_message[1]
        text_split_message = f"""Удалаем\n
        товар : <b>{product_name}</b>"""
        context.bot.send_message( id_user, text=text_split_message,  parse_mode='html' )
        key = 'remove_product'
        my_sqlbase( id_user, key, update, context )
    
    else: #остальной текст
        #text =('я вас не понял')
        #context.bot.send_message( id_user, text=text,  parse_mode='html' )
        url = f'https://yandex.ru/images/search?text=%D1%8F%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D0%BB%20%D1%82%D0%B5%D0%B1%D1%8F&from=tabbar&pos=0&img_url=http%3A%2F%2Frisovach.ru%2Fupload%2F2014%2F03%2Fmem%2Fmne-kazhetsya-ili-frai-futurama_46256504_orig_.jpg&rpt=simage&lr=171920'
        context.bot.send_photo( id_user, url )

    
    
     




    #print(f'id = {update.effective_chat.id}')

#start_handler = CommandHandler('start', start)