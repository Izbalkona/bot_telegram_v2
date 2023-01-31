from my_settings import *
from my_handlers import *

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot
from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler, BaseFilter, TypeHandler, ConversationHandler




def main() -> None:
    updater = Updater(telegram_token) #connect Telegam with token key
    updis = updater.dispatcher #rename for usability

    print(datetime.datetime.today().weekday())

    updis.add_handler(CommandHandler(('start', 'help'), start)) #покажет список команд
    updis.add_handler(CommandHandler('show', select_mysql)) #показать список покупок, количество, период
    updis.add_handler(CommandHandler('show_menu', show_menu))
    updis.add_handler(CommandHandler('clear', clear)) #clear полностью очистит вашу таблицу

    updis.add_handler(CommandHandler('show_sport', show_sport)) #показать дефолтный список товаров
    updis.add_handler(CommandHandler('show_sport', show_menu))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))# должно быть последним обрабатывает весь текст
    
    

    updater.start_polling() # цикл
    print('Started')
    updater.idle()

if __name__ == "__main__":
    main()