from flask import Flask

PORT = 8080
CERT_PATH = '/home/bassel/telegram_bot/ssl/fullchain.pem'
KEY_PATH = '/home/bassel/telegram_bot/ssl/privkey.pem'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main(*args, **kwargs):
    return "Welcome to our server!"

@app.route('/.well-known/acme-challenge/<challenge>')
def verify_challenge(challenge):
    challenge_file = open('.well-known/acme-challenge/' + challenge)
    return challenge_file.read()

if __name__ == '__main__':
    app.run('0.0.0.0', port=PORT, ssl_context=(CERT_PATH, KEY_PATH))