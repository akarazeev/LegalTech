from flask import Flask, render_template, request
from utils import get_data, get_jsdata
from myemail import send_email, make_html
import datetime
import typing

app = Flask(__name__)

# Read the data
data = get_data()
jsdata = get_jsdata()

# Getting cases
cases = ['-- Select the case --']
for id_assignment in jsdata:
    cases.append(' -'.join((id_assignment, jsdata[id_assignment]['Info']['Assigment name'])))

username = 'Anton Karazeev'
server_address = "http://10.100.23.13:5000"

with open('user_psswd_recipient.txt', 'r') as f:
    user = f.readline().strip()
    password = f.readline().strip()
    recipient = f.readline().strip()


@app.route('/login', methods=['get', 'post'])
def login_form():
    return render_template('login_form.html')


@app.route('/', methods=['get', 'post'])
def index():
    project_id = None

    if request.form:
        project_id = request.form.get('select_cases')
        project_id = project_id.split('-')[0].strip()
    else:
        project_id = '20120036'

    if project_id in jsdata.keys():
        info = jsdata[project_id]['Info']

        transactions = jsdata[project_id]['Transactions']
        transactions = list(transactions.values())

        # Sort the transactions by date
        transactions = sorted(transactions, key=lambda x: datetime.datetime.strptime(x['Entry Date'], '%Y-%m-%d'))

        total_for_transactions = '{:.2f}'.format(sum([trans['Total'] for trans in transactions]))

        return render_template('index_prod.html', cases=cases, query=project_id, transactions=transactions,
                               total_for_transactions=total_for_transactions,
                               info=info, username=username)
    else:
        return render_template('index_prod.html', cases=cases, query=project_id, not_found=True, username=username)


def is_email(address: str) -> bool:
    if "@" in address and len(address.split('@')) == 2 and '/' not in address:
        return True
    else:
        return False


@app.route('/form', methods=['get', 'post'])
def send_request():
    if request.form:
        subject = request.form.get('subject')
        body = request.form.get('body')
        address = request.form.get('address')

        print(subject, body)

        # Sending an email
        if is_email(address):
            yes_url = server_address + '/accept'
            modif_title = 'Re: {}'.format(subject)
            modifications_url = 'mailto:{}?subject={}&body=Original text: {}'.format(user, modif_title, body)
            html = make_html(subject, body, yes_url, modifications_url)
            send_email(user, password, address, subject, html)
        # Sending a message using chat-bot
        else:
            pass
        return render_template('request_form.html', sent=True, username=username)
    return render_template('request_form.html', username=username)


@app.route('/accept', methods=['get', 'post'])
def accept_request():
    return render_template('accept.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
