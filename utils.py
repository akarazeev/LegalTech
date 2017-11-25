# Requires file user_psswd_recipient.txt with: user, password, recipient on new lines

import urllib
import urllib.request
import requests
import sys
import email
import smtplib
from bs4 import BeautifulSoup
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = [recipient]
    SUBJECT = subject

    msg = MIMEMultipart("alternative")
    msg.set_charset("utf-8")

    msg["Subject"] = SUBJECT
    msg["From"] = FROM
    msg["To"] = TO[0]

    TEXT = MIMEText(body, "html", "utf-8")

    msg.attach(TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)

    server.sendmail(FROM, TO, msg.as_string())

    server.close()
    print("Success - {}".format(SUBJECT))


def make_html(title, text, yes_url, modifications_url):
    html = """\
    <html>
      <head></head>
      <body>
          <table>
              <tr>
                  <td align='center' colspan="2"><b style="font-size:20px">{}</b><br></td>
              </tr>
              <tr>
                  <td align='center' colspan="2">{}</td>
              </tr>
              <tr>
                  <td align='center' style="width:50px"><a href="{}">Yes</a></td>
                  <td align='center' style="width:50px"><a href="{}">Modifications</a></td>
              </tr>
          </table>
      </body>
    </html>

    """.format(title, text, yes_url, modifications_url)

    return html
