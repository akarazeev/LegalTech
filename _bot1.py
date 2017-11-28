from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, ParseMode
import logging
import json
import os
import numpy as np
import operator
<<<<<<< HEAD

=======
import time
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119


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
<<<<<<< HEAD
    'CHANGE': '6'
=======
    'CHANGE': '6',
    'LAWER': '7',
    'ASS': '8',
    'TIME': '9'
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
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
<<<<<<< HEAD
              InlineKeyboardButton("Next", callback_data=actions['NEXT'])]]

keyboard0 = [[InlineKeyboardButton("Show me last transaction", callback_data=actions['SHOW'])],
=======
              InlineKeyboardButton("Hours",  callback_data=actions['TIME']),
              InlineKeyboardButton("Next", callback_data=actions['NEXT'])]]

keyboard0 = [[InlineKeyboardButton("Lawer stats",  callback_data=actions['LAWER']),
              InlineKeyboardButton("Assignment stats",  callback_data=actions['ASS'])],
             [InlineKeyboardButton("Show me last transaction", callback_data=actions['SHOW'])],
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
             [InlineKeyboardButton("Choose transaction",  callback_data=actions['CHOOSE'])],
             [InlineKeyboardButton("Change assignment", callback_data=actions['CHANGE'])]]



def start(bot, update):
    if reg == 1:
        update.message.reply_text('Start working...')
<<<<<<< HEAD
        update.message.reply_text('Please, enter your assignment:')
=======
        #update.message.reply_text('Please, enter your assignment:')
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
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
<<<<<<< HEAD
        with open('json_2.crash', 'r') as f:
=======
        with open('json_4.json', 'r') as f:
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
            d = json.load(f)
        global lp
        lp = []
        for name, count in d[case]['Transactions'].items():
            for k in range(to_iterate):
<<<<<<< HEAD
                if count['n_transaction'] == k: 
=======
                if count['Transaction Number'] == k: 
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
                    lp.append((name, count, k))
                
        keyboard2 = [[InlineKeyboardButton("{}".format(j[0]), callback_data=j[0])] for j in lp]
        reply_markup = InlineKeyboardMarkup(keyboard2)
<<<<<<< HEAD
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
=======
        query.message.reply_text('Choose an action', reply_markup=reply_markup)
    
    elif query.data == actions['LAWER']:
        from legal_tech_utils import get_lawer_assignment_info
        with open('json_4.json', 'r') as f:
            d = json.load(f)
        responsible_name = d[case]['Info']['Responsible']
        lawer_assignment_info = get_lawer_assignment_info(responsible_name)  
        time.sleep(0.5)
        with open('plot11.png', 'rb') as f:
            query.message.reply_photo(photo=f)
        reply_markup = InlineKeyboardMarkup(keyboard0)
        query.message.reply_text('Choose something', reply_markup=reply_markup)
        
    elif query.data == actions['ASS']:
        from legal_tech_utils import plot_spents
        with open('json_4.json', 'r') as f:
            d = json.load(f)
        #responsible_name = d[case]['Info']['Responsible']
        lawer_assignment_info = plot_spents(case, '2018-01-01')  
        time.sleep(0.5)
        with open('piechart_paid.png', 'rb') as f:
            query.message.reply_photo(photo=f)
        reply_markup = InlineKeyboardMarkup(keyboard0)
        query.message.reply_text('Choose something', reply_markup=reply_markup)
        
    elif query.data == actions['TIME']:
        from legal_tech_utils import plot_hours_distribution
        with open('json_4.json', 'r') as f:
            d = json.load(f)
            
        for name, count in d[case]['Transactions'].items():
            if count['Transaction Number'] == to_iterate-iterator: 
                lt_name = name
                lt = count
                ltype = count['Transaction Type English']
        #responsible_name = d[case]['Info']['Responsible']
        lawer_assignment_info = plot_hours_distribution(ltype) 
        time.sleep(0.5)
        with open('distplot_hours.png', 'rb') as f:
            query.message.reply_photo(photo=f)
        reply_markup = InlineKeyboardMarkup(keyboard0)
        query.message.reply_text('Choose something', reply_markup=reply_markup)

    # change case
    elif query.data == actions['CHANGE']:
        query.message.reply_text('Start working...')
        query.message.reply_text('Please, choose of your possible assignments:')
        global ass
        with open('dict_code.json', 'r') as f:
            d = json.load(f)
        #update.message.reply_text('Great 2!')
        ass = []
        for name, k in d[code].items():
                ass.append((name, k))
                
        keyboard3 = [[InlineKeyboardButton("{}".format(j[0]), callback_data=j[0])] for j in ass]
        reply_markup = InlineKeyboardMarkup(keyboard3)
        query.message.reply_text('Choose an ass', reply_markup=reply_markup)
        
    # prev case
    if query.data == actions['PREV']:
        #bot.edit_message_text(text="",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
        #bot.edit_message_text(text="Ok, prev",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
        #bot.edit_message_text(text="",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
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
<<<<<<< HEAD
        bot.edit_message_text(text="Ok, next",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
=======
        #bot.edit_message_text(text="",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
        #bot.edit_message_text(text="Ok, next",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
        #bot.edit_message_text(text="",
        #                      chat_id=query.message.chat_id,
        #                      message_id=query.message.message_id)
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
        if iterator > 0:
            iterator -= 1
            # bot.send_message(query.message.chat_id, to_iterate[iterator])
            send_transaction(query)
        else:
            bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')

        reply_markup = InlineKeyboardMarkup(keyboard1)
        query.message.reply_text('Choose something', reply_markup=reply_markup)

<<<<<<< HEAD
    for j in lp:
            if query.data == j[0]:
                #update.message.reply_text('{} {}'.format(to_iterate, j[3]), parse_mode=ParseMode.HTML)
                iterator = to_iterate - j[2]
                send_transaction(query)
                #bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')

                reply_markup = InlineKeyboardMarkup(keyboard1)
                query.message.reply_text('Choose something', reply_markup=reply_markup)
=======
    
    for i in ass:
                #query.message.reply_text('Ya tut1 {} {}'.format(query.data, ass[0]))
                if query.data == i[0]:
                    #query.message.reply_text('Ya tut2')
                    case = str(i[1])
                    with open('json_4.json', 'r') as f:
                        d = json.load(f)
                        
                        to_iterate = np.max([d[case]['Transactions'][j]['Transaction Number'] for j in list(d[case]['Transactions'].keys())])

                        query.message.reply_text('Info for your assignment: ')#{}'.format(d[case]['Info']))

                        sorted_x = sorted(d[case]['Info'].items(), key=operator.itemgetter(0))
                        #sorted_counts = sorted(d[case]['Info'].items(), key=lambda x: x[1], reverse=True)
                        for name, count in sorted_x:
                            if count == count: query.message.reply_text(text = '{}: <b>{}</b>'.format(name, count), parse_mode=ParseMode.HTML)

                        from legal_tech_utils import gen_status_bar
                        st_bar = gen_status_bar(case, '2008-08-30')
                        query.message.reply_text('Progress:  <i>{}%</i>'.format(st_bar['percent'].split('\\')[0]), parse_mode=ParseMode.HTML)
                        with open(st_bar['filepath'], 'rb') as f:
                            query.message.reply_photo(photo=f)

                            reply_markup = InlineKeyboardMarkup(keyboard0)
                            #update.message.reply_text('Progress:  <b>{}</b>'.format(st_bar['percent']))
                            query.message.reply_text('Choose something', reply_markup=reply_markup)
                
    for j in lp:
        if query.data == j[0]:
            #update.message.reply_text('{} {}'.format(to_iterate, j[3]), parse_mode=ParseMode.HTML)
            iterator = to_iterate - j[2]
            send_transaction(query)
            #bot.send_message(query.message.chat_id, 'The End. Now send me another keyword')

            reply_markup = InlineKeyboardMarkup(keyboard1)
            query.message.reply_text('Choose something', reply_markup=reply_markup)
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119

def send_transaction(update):
    chat_id = str(update.message.chat_id)

<<<<<<< HEAD
    with open('json_2.crash', 'r') as f:
        d = json.load(f)
    
    for name, count in d[case]['Transactions'].items():
         if count['n_transaction'] == to_iterate-iterator: 
                lt_name = name
                lt = count
                
=======
    with open('json_4.json', 'r') as f:
        d = json.load(f)
    
    for name, count in d[case]['Transactions'].items():
         if count['Transaction Number'] == to_iterate-iterator: 
                lt_name = name
                lt = count
    global graph
    graph = lt
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
    update.message.reply_text('<b>Transaction:      {}</b>'.format(lt_name), parse_mode=ParseMode.HTML)
    for name, count in lt.items():
            if count == count: update.message.reply_text(text = '{}: <b>{}</b>'.format(name, count), parse_mode=ParseMode.HTML)


def rules_fun(bot, update):

    global to_iterate
<<<<<<< HEAD
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
=======
    to_iterate = 0
    global iterator
    global ass
    global lp
    lp = []
    iterator = 0
    global case
    global reg
    global code
    case = update.message.text
    print('{}'.format(reg))
    if reg == 0 and case in ['lol', 'kek']: 
        
        update.message.reply_text('Great!')
        reg = 1
        code = case
        #start(bot, update)
        
        chat_id = str(update.message.chat_id)
        
        with open('dict_code.json', 'r') as f:
            d = json.load(f)
        #update.message.reply_text('Great 2!')
        ass = []
        for name, k in d[code].items():
                ass.append((name, k))
                
        keyboard3 = [[InlineKeyboardButton("{}".format(j[0]), callback_data=j[0])] for j in ass]
        reply_markup = InlineKeyboardMarkup(keyboard3)
        update.message.reply_text('Choose an ass', reply_markup=reply_markup)
        
        
    elif reg == 0 and case not in ['lol', 'kek']: 
        update.message.reply_text('Wrong!')
        start(bot, update)
    else:
        
        code = case
        #start(bot, update)
        
        chat_id = str(update.message.chat_id)
        
        with open('dict_code.json', 'r') as f:
            d = json.load(f)
        #update.message.reply_text('Great 2!')
        ass = []
        for name, k in d[code].items():
                ass.append((name, k))
                
        keyboard3 = [[InlineKeyboardButton("{}".format(j[0]), callback_data=j[0])] for j in ass]
        reply_markup = InlineKeyboardMarkup(keyboard3)
        update.message.reply_text('Choose an ass', reply_markup=reply_markup)
>>>>>>> 78a0d9134bccf9852b13f5c60ed0d0db94a5e119
        

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
