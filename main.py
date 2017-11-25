from flask import Flask, render_template, request
from utils import send_email, make_html
import json

app = Flask(__name__)

with open('user_psswd_recipient.txt', 'r') as f:
    user = f.readline().strip()
    password = f.readline().strip()
    recipient = f.readline().strip()


to_email = 'anton.karazeev@gmail.com'
lawyer_mail = user
server_address = 'http://10.100.23.13:5002'


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        text = request.form.get('query')
        print(text)

        # Send a message
        title = 'Something urgent'
        yes_url = server_address + '/reply' + '/42'

        modif_title = 'Modification: {}'.format(title)
        modifications_url = 'mailto:{}?subject={}&body=Original text: {}'.format(lawyer_mail, modif_title, text)

        html = make_html(title, text, yes_url, modifications_url)
        send_email(user, password, to_email, title, html)

        return "The message has been sent!"
        # return render_template('index.html', query=text)

    return render_template('index.html')


@app.route('/t/<phrase>', methods=['get'])
def translate_phrase(phrase):
    phrase = phrase.replace('+', ' ')

    final_json = json.dumps({'phrase': phrase})

    return final_json


@app.route('/reply/<token>', methods=['get'])
def reply(token):
    print(token)
    return 'Accepted!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)
