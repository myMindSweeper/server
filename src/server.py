from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from os import environ
from flask import Flask, request
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime

from db import session
from db.models import User, MessageThread, Message
from utils.messenger_scraper import scrapePage

app = Flask(__name__)
CORS(app)

@app.route('/create-account', methods=['POST'])
def create_account():
    body = request.get_json()
    token = body.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), environ.get("GOOGLE_CLIENT_ID"))
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer')
        userid = idinfo['sub']
        new_user = User(id=userid)
        session.add(new_user)
        session.commit()
        return 'Succesful'
    except Exception as e:
        return str(e), 400

@app.route('/upload-fb', methods=['POST'])
def upload_fb():
    body = request.get_json()
    token = body.get('token')
    files = body.get('files')
    thread_id = body.get('thread_id')
    i = 0
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), environ.get("GOOGLE_CLIENT_ID"))
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer')
        userid = idinfo['sub']
        user = session.query(User).filter(User.id==userid).one()
        for text in files:
            try:
                new_thread = MessageThread(id=thread_id, user_id=user.id, person=str(i))
                session.add(new_thread)
                try:
                    session.commit()
                except:
                    session.rollback()
                p, msgs = scrapePage(str(i), text.replace(' EDT', '').replace(' EST', ''))
                for m in msgs:
                    date = datetime.fromtimestamp(m)
                    msg = Message(thread_id=new_thread.id, type='FB', body=m['body'],
                        date=date, user_speaking=m['user_speaking'])
                    session.add(msg)
            except:
                pass
            i += 1
        try:
            session.commit()
        except:
            session.rollback()
    except Exception as e:
        session.rollback()
        return str(e) + 'threadid:' + str(sms_thread_id)

@app.route('/upload-sms', methods=['POST'])
def upload_sms():
    body = request.get_json()
    token = body.get('token')
    sms_thread_id = body.get('thread_id')
    person = body.get('person')
    sms_list = body.get('sms_list')
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), environ.get("GOOGLE_CLIENT_ID"))
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer')
        userid = idinfo['sub']
        user = session.query(User).filter(User.id==userid).one()
        new_thread = MessageThread(id=sms_thread_id, user_id=user.id, person=person)
        session.add(new_thread)
        try:
            session.commit()
        except:
            session.rollback()
        for sms in sms_list:
            date = datetime.fromtimestamp(sms['date'] / 1000.0)
            msg = Message(thread_id=new_thread.id, type='SMS', body=sms['body'],
                date=date, user_speaking=sms['user_speaking'])
            session.add(msg)
        session.commit()
        return 'Succesful'
    except Exception as e:
        session.rollback()
        return str(e) + 'threadid:' + str(sms_thread_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(environ.get('SERVER_PORT')))
