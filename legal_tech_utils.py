import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import json

from labella.timeline import TimelineSVG, TimelineTex
from labella.utils import COLOR_10
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import catboost as cb
import subprocess

cbr = cb.CatBoostRegressor()
cbr.load_model('catboost_model')
average_len_dict = json.load(open('average_len_dict'))
lawer_counts = pd.read_csv('lawer_counts.csv')
df_lawer_assignment_price = pd.read_csv('df_lawer_assignment_price.csv').set_index(['Responsible', 'Assignment Type'])
df_lawer_price = pd.read_csv('df_lawer_price.csv').set_index('Responsible')
df_assignment_price = pd.read_csv('df_assignment_price.csv').set_index(['Assignment Type'])

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly
import plotly.graph_objs

df = pd.read_csv('content.csv')
DATE_FORMAT = '%Y-%m-%d'

df['status_date'] = df['Entry Date'].apply(lambda x: datetime.strptime(x, DATE_FORMAT))
df['Assignment'] = df['Assignment'].astype(str)

options = {
    'initialWidth': 800,
    'initialHeight': 250,
    'direction': 'down',
    'dotColor': COLOR_10,
    'labelBgColor': COLOR_10,
    'linkColor': COLOR_10,
    'textFn': lambda x: x['text'] + ' - ' + str(x['time'].year),
    'labelPadding': {'left': 0, 'right': 0, 'top': 1, 'bottom': 1},
    'margin': {'left': 20, 'right': 20, 'top': 20, 'bottom': 20},
    'layerGap': 40,
    'labella': {
        'nodeHeight': 12,
    },
    'showTicks': True
}

def aggregator(rec):
    result = ""
    for key, value in rec['Transaction'].iteritems():
        result = result + value + '; '
    return result[:-2]

def get_timeline(assignment_id, current_date, name='timeline'):
    mask_1 = df['Assignment'] == assignment_id
    mask_2 = df['Entry Date'] <= current_date
    max_date = df.loc[mask_1, 'Entry Date'].max()
    mask = mask_1 & mask_2
    df_small = df.loc[mask, ['Transaction', 'status_date']]

    tmp = df_small.groupby(['status_date'], as_index=True).apply(aggregator).reset_index()

    tmp = tmp.rename(
        columns={
            0: 'status'
        }
    )

    items = [
        {'time': rec[1]['status_date'], 'text': rec[1]['status']} for rec in tmp.iterrows()
    ]

    # print(f'max_date is {max_date}, current_date is {current_date}')
    if current_date < max_date:
        # print('True')
        today_dict = {
            'time': datetime.strptime(current_date, DATE_FORMAT),
            'text': 'Today',
        }
        items.append(today_dict)

    if len(items) == 1:
        print('Only one sample')
        return tmp.loc[0, 'status_date'], tmp.loc[0, 'status']

    tl = TimelineTex(items, options=options)

    pdf_filename = f'{name}.pdf'
    command = 'convert -verbose -density 500 "{}" -quality 100 "{}"'.format(pdf_filename, pdf_filename.replace('.pdf', '.png'))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = p.communicate()

def gen_status_bar(assignment, current_date, filepath = 'progress_bar.png'):
    # def get_history_len(assignment, current_date):
    is_ended = False
    mask_assignment = (df['Assignment'] == assignment)
    #     print(current_date)
    #     is_ended, n_days = get_history_len('1', current_date)
    #     try:
    mask = mask_assignment & (df.loc[mask_assignment, 'Entry Date'] < current_date)
    max_index = df.index[mask].max()
    transaction = df.loc[max_index, 'Transaction Type Englis']
    min_date = df.loc[mask, 'Entry Date'].min()
    min_date = datetime.strptime(min_date, DATE_FORMAT)
    max_date = df.loc[mask_assignment, 'Entry Date'].max()
    max_date = datetime.strptime(max_date, DATE_FORMAT)
    current_date = datetime.strptime(current_date, DATE_FORMAT)
    is_ended = current_date > max_date
    n_days = (min(current_date, max_date) - min_date).days
    #     return is_ended, result
    if is_ended:
        percent = 100
    else:
        percent = int(100 * average_len_dict[transaction] / (average_len_dict[transaction] + n_days))
    # except:
    #         percent = 0

    plt.figure(figsize=(10, 1))
    plt.barh(0.05, 100, height=0.1, color='#95bef4')
    plt.barh(0.05, percent, height=0.1, color='#0ba550')
    plt.xlim(0, 100)
    plt.ylim(0, 0.1)
    plt.tick_params(
        axis='y',
        which='both',  # both major and minor ticks are affected
        left='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelleft='off')
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')  # labels along the bottom edge are off
    plt.axvline(percent, color='orange')
    plt.savefig(filepath)

    return {
        'percent': str(percent) + '\%',
        'filepath': filepath,
    }

# init_notebook_mode(connected=True)
def get_lawer_assignment_info(responsible_name, transaction_name, filepath = 'plot_image.jpeg'):
    if os.path.exists(filepath):
        os.remove(filepath)
    mean_lawer_price = int(df_lawer_price.loc[responsible_name, 'Hour Price'])
    mean_assignment_price = int(df_assignment_price.loc[transaction_name, 'Hour Price'])
    mean_lawer_assignment_price = int(df_lawer_assignment_price.loc[(responsible_name, transaction_name), 'Hour Price'])

    result = {
        'mean_lawer_price': mean_lawer_price,
        'mean_assignment_price': mean_assignment_price,
        'mean_lawer_assignment_price': mean_lawer_assignment_price,
    }

    mask_lawer = lawer_counts['Responsible'] == responsible_name
    assignment_types = lawer_counts.loc[mask_lawer, 'Assignment Type'].values
    hour_prices = lawer_counts.loc[mask_lawer, 'Hour Price'].values

    #     filename = f'/Users/smerdov/Junction2017/{responsible_name}.html'
    #     filename = '/Users/smerdov/Junction2017/Piechart.html'


    fig = plotly.offline.plot(
        {
            "data": [
                plotly.graph_objs.Pie(labels=assignment_types, values=hour_prices)
            ]
        },
        #         filename = filename,
        image='jpeg',
    )

    #     py.image.save_as(fig, filename='a-simple-plot.png')

    return result

def get_catboost_predict(assignment_id, current_date):
    # assignment_id = '20080029'
    mask_1 = df['Assignment'] == assignment_id
    mask_2 = df['Entry Date'] <= current_date
    mask = mask_1 & mask_2
    small_df = df.loc[mask, ['Transaction']]
    try:
        max_index = df.index[mask].max()
        max_date = df.loc[mask_1, 'Entry Date'].max()
        paid_series = df.loc[mask, 'Paid']
        paid_sum = paid_series.sum() - paid_series[max_index]
        paid_count = len(paid_series) - 1
        data_to_predict = [
            df.loc[max_index, 'Transaction'],
            df.loc[max_index, 'Transaction Type Englis'],
            paid_sum,
            paid_count
        ]
        # print(data_to_predict)
        data_to_predict = cb.Pool([data_to_predict], cat_features=[0,1])
        prediction = int(cbr.predict(data_to_predict)[0])
    except:
        prediction = 1000
    return prediction

if __name__ == '__main__':
    get_timeline('1', '2008-08-30')
    gen_status_bar('12', '2008-10-23')
    responsible_name = 'Boris Keilaniemi'
    transaction_name = 'Rahoitusoikeus'
    lawer_assignment_info = get_lawer_assignment_info(responsible_name, transaction_name)

    catboost_prediction = get_catboost_predict(assignment_id, '2017-01-01')
