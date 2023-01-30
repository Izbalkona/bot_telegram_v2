from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler

from my_sql import *


def create_new_user(update, context):
    

    print(update.message.chat.username)
    print('Новый пользователь создан')


def start(update, context):
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text='dn',  parse_mode='html')

def insert_mysql(update, context): #внести данные
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text='dn',  parse_mode='html')

def select_mysql(update, context): #вывести данные
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text='dn',  parse_mode='html')
    
def echo(update, context) -> None: #регистрация любого сообщения
    id_users = update.effective_chat.id

def add_table(update, context): #добавить таблицу
    id_user = update.effective_chat.id
    key='add_table'
    my_sqlbase(id_user, key, update, context) #key это ключ к сценарию
    
    
     




    #print(f'id = {update.effective_chat.id}')

#start_handler = CommandHandler('start', start)