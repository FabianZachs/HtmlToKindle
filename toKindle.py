import os
import sys
import json
import pdfkit
import getpass
import email, smtplib, ssl

from bs4 import BeautifulSoup
from  urllib.request import Request, urlopen
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://realpython.com/python-send-email/

port = 465
smtp_server = "smtp.gmail.com"

def print_usage():
    print('Usage:')
    print('\tpython3 ' + sys.argv[0] + ' <link>')

def hello_message():
    print(r'''
      _   _ _____ __  __ _           __    _  ___           _ _      
     | | | |_   _|  \/  | |      ____\ \  | |/ (_)_ __   __| | | ___ 
     | |_| | | | | |\/| | |     |_____\ \ | ' /| | '_ \ / _` | |/ _ \
     |  _  | | | | |  | | |___  |_____/ / | . \| | | | | (_| | |  __/
     |_| |_| |_| |_|  |_|_____|      /_/  |_|\_\_|_| |_|\__,_|_|\___|
    ''')

def get_credentials():
    with open('creds.json', 'r') as json_file:
        data = json.load(json_file)
        sender_email = data['sender_email']
        kindle_email = data['kindle_email']
        print('Email: ' + sender_email)
        sender_password = getpass.getpass()
    return sender_email, sender_password, kindle_email


def get_article_title(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    return soup.title.string;


def generate_pdf(filename, link):
    pdfkit.from_url(link, filename)


def send_pdf_to_kindle(sender_email, sender_password, kindle_email, filename):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = kindle_email

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, kindle_email, text)

def create_proper_filename(filename):
    symbols = [' ', '\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for symbol in symbols:
        filename = filename.replace(symbol, "_")
    return filename

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_usage()
        exit(1)
    link = sys.argv[1]
    hello_message()
    sender_email, sender_password, kindle_email = get_credentials()
    filename = create_proper_filename(get_article_title(link) + '.pdf')
    print('You are sending: ' + filename)
    generate_pdf(filename, link)
    send_pdf_to_kindle(sender_email, sender_password, kindle_email, filename)
    os.remove(filename)
