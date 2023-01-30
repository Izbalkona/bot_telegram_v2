from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler

from my_sql import *


#def create_new_user(update, context):
    #print(update.message.chat.username)
    #print('Новый пользователь создан')


def start(update, context):
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text="""
    /show - показать список покупок, количество, период
    чтобы добавить товар, просто напишите по форме
    название кол-во период в днях
    пример
    картошка 5кг 4
    чтобы удалить продукт поставьте знак - название
    пример
    - картошка""" ,  parse_mode='html' )



def select_mysql(update, context): #показать список покупок
    id_user = update.effective_chat.id
    key='show_my_table'
    result = my_sqlbase(id_user, key, update, context) #key это ключ к сценарию
    for product in result:
        text= f"""{product['product_name']} : {product['weight_count']} : {product['period_day']}"""
        print(text)
        context.bot.send_message( id_user, text=text ,  parse_mode='html' )
    
def echo(update, context) -> None: #регистрация любого сообщения, предлагаем каждую строчку добавить в таблицу, предварительно распарсив текст
    id_user = update.effective_chat.id
    split_message = update.message.text.split()
    if len(split_message) == 3:
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

    elif split_message[0] == '-':
        product_name = split_message[1]
        text_split_message = f"""Удалаем\n
        товар : <b>{product_name}</b>"""
        context.bot.send_message( id_user, text=text_split_message,  parse_mode='html' )
        key = 'remove_product'
        my_sqlbase( id_user, key, update, context )
    
    else:
        text =('я вас не понял')
        context.bot.send_message( id_user, text=text,  parse_mode='html' )


def add_table(update, context): #добавить таблицу
    id_user = update.effective_chat.id
    key='add_table'
    my_sqlbase(id_user, key, update, context) #key это ключ к сценарию
    
    
     




    #print(f'id = {update.effective_chat.id}')

#start_handler = CommandHandler('start', start)