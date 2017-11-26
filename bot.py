from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, ParseMode
import logging
import json
import os
import numpy as np
import operator



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

actions = {
    'NEXT':   '1',
    'PREV':   '2',
    'SEARCH': '3',
    'SHOW': '4',
    'CHOOSE': '5',
    'CHANGE': '6'
}

iterator = 0
reg = 0
is_searching = False
to_iterate = None

# ------------------ #
#  Here goes bot's   #
#  Implementation    #
# ------------------ #


def check_auth(func):
    def wrapper(uid):
        if reg:
             func()
        else:
            pass


def get_token():
    path = 'token.json'
    with open(path, 'r') as jsn:
        data = json.load(jsn)
    return data['token']


keyboard1 = [[InlineKeyboardButton("Choose transaction",  callback_data=actions['CHOOSE'])],
             [InlineKeyboardButton("Change assignment", callback_data=actions['CHANGE'])],
             [InlineKeyboardButton("Previous", callback_data=actions['PREV']),
              InlineKeyboardButton("Next", callback_data=actions['NEXT'])]]

keyboard0 = [[InlineKeyboardButton("Show me last transaction", callback_data=actions['SHOW'])],
             [InlineKeyboardButton("Choose transaction",  callback_data=actions['CHOOSE'])],
             [InlineKeyboardButton("Change assignment", callback_data=actions['CHANGE'])]]



def start(bot, update):
    if reg == 1:
        update.message.reply_text('Start working...')
        update.message.reply_text('Please, enter your assignment:')
    elif reg == 0:
        update.message.reply_text('Your code')
        

def button(bot, update):
    global iterator
    global to_iterate
    global iterator
    global case

    query = update.callback_query
    
    # SHOW case
    if query.data == actions['SHOW']:
        
        send_transaction(query)
        #bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')
        
        reply_markup = InlineKeyboardMarkup(keyboard1)
        query.message.reply_text('Choose something', reply_markup=reply_markup)

    # CHOOSE case
    elif query.data == actions['CHOOSE']:
        with open('json_2.crash', 'r') as f:
            d = json.load(f)
        global lp
        lp = []
        for name, count in d[case]['Transactions'].items():
            for k in range(to_iterate):
                if count['n_transaction'] == k: 
                    lp.append((name, count, k))
                
        keyboard2 = [[InlineKeyboardButton("{}".format(j[0]), callback_data=j[0])] for j in lp]
        reply_markup = InlineKeyboardMarkup(keyboard2)
        query.message.reply_text('Choose transaction', reply_markup=reply_markup)
        
       
    
    # change case
    elif query.data == actions['CHANGE']:
        query.message.reply_text('Start working...')
        query.message.reply_text('Please, enter your assignment:')
        
        iterator = 0

        case = query.message.text
        chat_id = str(query.message.chat_id)

        with open('json_2.crash', 'r') as f:
            d = json.load(f)
        to_iterate = np.max([d[case]['Transactions'][j]['n_transaction'] for j in list(d[case]['Transactions'].keys())])
        query.message.reply_text('Info for your assignment: ')#{}'.format(d[case]['Info']))

        reply_markup = InlineKeyboardMarkup(keyboard0)

        query.message.reply_text('Choose something', reply_markup=reply_markup)
        
    # prev case
    if query.data == actions['PREV']:
        bot.edit_message_text(text="Ok, prev",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        #bot.send_message(query.message.chat_id, '--------------------------')
        if iterator+1 < to_iterate:
            iterator += 1
            # bot.send_message(query.message.chat_id, to_iterate[iterator])
            send_transaction(query)
        else:
            bot.send_message(query.message.chat_id, 'Move Next please')
        reply_markup = InlineKeyboardMarkup(keyboard1)
        query.message.reply_text('Choose something', reply_markup=reply_markup)

    # SEARCH case
    elif query.data == actions['SEARCH']:
        bot.edit_message_text(text="Ok, send me a keyword",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        is_searching = True

    # next case
    elif query.data == actions['NEXT']:
        bot.edit_message_text(text="Ok, next",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        if iterator > 0:
            iterator -= 1
            # bot.send_message(query.message.chat_id, to_iterate[iterator])
            send_transaction(query)
        else:
            bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')

        reply_markup = InlineKeyboardMarkup(keyboard1)
        query.message.reply_text('Choose something', reply_markup=reply_markup)

    for j in lp:
            if query.data == j[0]:
                #update.message.reply_text('{} {}'.format(to_iterate, j[3]), parse_mode=ParseMode.HTML)
                iterator = to_iterate - j[2]
                send_transaction(query)
                #bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')

                reply_markup = InlineKeyboardMarkup(keyboard1)
                query.message.reply_text('Choose something', reply_markup=reply_markup)

def send_transaction(update):
    chat_id = str(update.message.chat_id)

    with open('json_2.crash', 'r') as f:
        d = json.load(f)
    
    for name, count in d[case]['Transactions'].items():
         if count['n_transaction'] == to_iterate-iterator: 
                lt_name = name
                lt = count
                
    update.message.reply_text('<b>Transaction:      {}</b>'.format(lt_name), parse_mode=ParseMode.HTML)
    for name, count in lt.items():
            if count == count: update.message.reply_text(text = '{}: <b>{}</b>'.format(name, count), parse_mode=ParseMode.HTML)


def rules_fun(bot, update):

    global to_iterate
    global iterator
    iterator = 0
    global case
    global reg
    case = update.message.text
    print('{}'.format(reg))
    if reg == 0 and case == 'lol': 
        update.message.reply_text('Great!')
        reg = 1
        start(bot, update)
    elif reg == 0 and case != 'lol': 
        update.message.reply_text('Wrong!')
        start(bot, update)
    else:
        case = update.message.text

        chat_id = str(update.message.chat_id)

        with open('json_2.crash', 'r') as f:
            d = json.load(f)
        to_iterate = np.max([d[case]['Transactions'][j]['n_transaction'] for j in list(d[case]['Transactions'].keys())])

        update.message.reply_text('Info for your assignment: ')#{}'.format(d[case]['Info']))

        sorted_x = sorted(d[case]['Info'].items(), key=operator.itemgetter(0))
        #sorted_counts = sorted(d[case]['Info'].items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_x:
                if count == count: update.message.reply_text(text = '{}: <b>{}</b>'.format(name, count), parse_mode=ParseMode.HTML)

        reply_markup = InlineKeyboardMarkup(keyboard0)

        update.message.reply_text('Choose something', reply_markup=reply_markup)
        

def help_function(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error_arg):
    logger.warning('Update "%s" caused error "%s"' % (update, error_arg))


def main():
    updater = Updater(get_token())
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_function))
    dp.add_error_handler(error)

    # on non-command messages
    dp.add_handler(MessageHandler(Filters.text, rules_fun))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("-> Hi!")
    main()
