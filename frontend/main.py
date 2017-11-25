from flask import Flask, render_template, request
from utils import get_data, get_jsdata
import datetime

app = Flask(__name__)
data = get_data()
jsdata = get_jsdata()

authors = sorted(list(set(data['Author / Tekijä'].values)))
cases = list(jsdata.keys())


@app.route('/login', methods=['get', 'post'])
def login_form():
    # return render_template('index_prod.html')
    return render_template('login_form.html')

    ########################
    # if request.form:
    #     query = request.form.get('query')
    #     print(request.form.get('select'))
    #     entries = process_query(query, df)
    #     print(len(entries))
    #     return render_template('index.html', authors=authors, cases=cases, query=query, entries=entries)
    ##############################

    # return render_template('index.html', authors=authors, cases=cases,
    #                        transactions=transactions, total_for_transactions=total_for_transactions,
    #                        info=info)


@app.route('/', methods=['get', 'post'])
def index():
    username = 'Anton Karazeev'
    project_id = '20120036'

    if request.form:
        project_id = request.form.get('query')

    if project_id in jsdata:
        info = jsdata[project_id]['Info']

        transactions = jsdata[project_id]['Transactions']
        transactions = list(transactions.values())

        # Sort the transactions by date
        transactions = sorted(transactions, key=lambda x: datetime.datetime.strptime(x['Entry Date'], '%Y-%m-%d'))

        total_for_transactions = '{:.2f}'.format(sum([trans['Total'] for trans in transactions]))

        return render_template('index_prod.html', query=project_id, transactions=transactions,
                               total_for_transactions=total_for_transactions,
                               info=info, username=username)
    else:
        return render_template('index_prod.html', query=project_id, not_found=True, username=username)

if __name__ == '__main__':
    app.run(debug=True)
