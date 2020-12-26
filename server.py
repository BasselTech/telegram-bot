from flask import Flask, request
import requests
import time

from message import Message

PORT = 8080
CERT_PATH = '/home/bassel/telegram_bot/ssl/fullchain.pem'
KEY_PATH = '/home/bassel/telegram_bot/ssl/privkey.pem'

TELEGRAM_TOKEN = '1427190815:AAEV4kyzuxGz4r4-Z1ql3V76mTuEbhQ9qeI'
API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' + '/{method_name}'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main(*args, **kwargs):
    message = Message(request.json['message'], TELEGRAM_TOKEN)
    method_name, params = message.get_response()
    while not send_response(method_name, params):
        time.sleep(5)
    return "OK"

def send_response(method_name, params):
    if method_name == 'sendDocument':
        document = params['document']
        del params['document']
        r = requests.post(url=API_URL.format(method_name=method_name), params=params, files={'document': document})
    else:
        r = requests.post(url=API_URL.format(method_name=method_name), params=params)
    return r.status_code == 200

@app.route('/.well-known/acme-challenge/<challenge>')
def verify_challenge(challenge):
    challenge_file = open('.well-known/acme-challenge/' + challenge)
    return challenge_file.read()

if __name__ == '__main__':
    app.run('0.0.0.0', port=PORT, ssl_context=(CERT_PATH, KEY_PATH))