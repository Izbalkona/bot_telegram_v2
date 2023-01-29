from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler






def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message( chat_id, text='dn',  parse_mode='html')

def insert_mysql(update, context): #
    chat_id = update.effective_chat.id
    context.bot.send_message( chat_id, text='dn',  parse_mode='html')

def select_mysql(update, context): #
    chat_id = update.effective_chat.id
    context.bot.send_message( chat_id, text='dn',  parse_mode='html')
    
def echo(update, context) -> None: #регистрация любого сообщения
    chat_id = update.effective_chat.id

    print(f'id = {update.effective_chat.id}')

#start_handler = CommandHandler('start', start)