#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging 

from my_settings import *
from my_handlers import *

from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler
 

def main() -> None:
    updater = Updater(telegram_token) #connect Telegam with token key
    updis = updater.dispatcher #rename for usability





    updis.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))# должно быть последним


    updater.start_polling() # цикл
    print('Started')
    updater.idle()
       
if __name__ == "__main__":
    main()