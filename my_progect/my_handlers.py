from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler

from my_sql import *

from my_settings import *
#def create_new_user(update, context):
    #print(update.message.chat.username)
    #print('Новый пользователь создан')


def start(update, context):
    id_users = update.effective_chat.id
    context.bot.send_message( id_users, text="""
    1. /day - укажите в какой день вы ходите за покупками\n
    2. /show - показать список покупок, количество, период\n
    3. чтобы добавить товар, просто напишите по форме\n
    название кол-во период в неделях\n
    пример\n
    картошка 5кг 4\n
    4. чтобы удалить продукт поставьте знак - название\n
    пример\n
    - картошка\n
    5. /clear полностью очистит вашу таблицу""" ,  parse_mode='html' )


def clear(update, context): #показать список покупок
    id_user = update.effective_chat.id
    key = 'clear'
    my_sqlbase(id_user, key, update, context) #key это ключ к сценарию


def select_mysql(update, context): #показать список покупок
    id_user = update.effective_chat.id
    key = 'show_my_table'
    result = my_sqlbase(id_user, key, update, context) #key это ключ к сценарию
    for product in result:
        text= f"""{product['product_name']} : {product['weight_count']} : {product['period_day']}"""
        print(text)
        context.bot.send_message( id_user, text=text ,  parse_mode='html' )
        
         
def echo(update, context) -> None: #регистрация любого сообщения, предлагаем каждую строчку добавить в таблицу, предварительно распарсив текст
    id_user = update.effective_chat.id
    logging.info(f'запрос пользователя {id_user} : {update.message.text}')
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


    
    
     




    #print(f'id = {update.effective_chat.id}')

#start_handler = CommandHandler('start', start)