#!/usr/bin/python3
# -*- coding: utf-8 -*-



from my_settings import *
from my_handlers import *

from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler
 

def main() -> None:
    updater = Updater(telegram_token) #connect Telegam with token key
    updis = updater.dispatcher #rename for usability


    updis.add_handler(CommandHandler('show', select_mysql)) #показать список покупок, количество, период

    updis.add_handler(CommandHandler('start', start)) #покажет список команд
    updis.add_handler(CommandHandler('clear', clear)) #clear полностью очистит вашу таблицу

    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))# должно быть последним обрабатывает весь текст

    updater.start_polling() # цикл
    print('Started')
    updater.idle()
       
if __name__ == "__main__":
    main()