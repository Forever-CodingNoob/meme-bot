from pymessenger.bot import Bot
from flask import Flask,request,render_template
from flask_socketio import SocketIO,send,emit
import os
import json
from .bot_react import MemeBot,MemeSOCKET
from threading import Thread

'''load secret tokens(.env file is not uploaded for preventing revealing the secret tokens inside, hence setting environment variables on cloud platform is a must):
'''
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.abspath(__file__),'..\\..\\.env'))
'''
'''

PAGE_ACCESS_TOKEN=os.environ['PAGE_ACCESS_TOKEN']
VERIFICATION_TOKEN=os.environ['VERIFICATION_TOKEN']

app=Flask(__name__)
bot=Bot(PAGE_ACCESS_TOKEN)
io=SocketIO(app=app,logger=True,engineio_logger=False,async_mode='eventlet')
app.config['DEBUG']=True

@app.route('/callback',methods=('GET',))
def verify():
    print('get query strings:',request.args)
    if request.args.get('hub.mode')=='subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token')==VERIFICATION_TOKEN:
            return request.args["hub.challenge"], 200
        return 'verification_token mismatch!',403
    return 'hola',200
@app.route('/callback',methods=('POST',))
def webhook():
    print('get message:',repr(request.data))
    data=json.loads(request.data)
    print('parsed messege:\n',json.dumps(data, indent=4, sort_keys=True))
    for entry in data.get('entry'):
        for message in entry.get('messaging'):
            if message.get('message'):
                sender_id = message['sender']['id']
                recipient_id = message['recipient']['id']
                if msg_text:=message['message'].get('text'):
                    print('get text:',msg_text)
                    if msg_text=="ㄛㄛ":
                        bot.send_text_message(sender_id,msg_text)
                        continue
                    MemeBot(msg_text,bot=bot,sender_id=sender_id).send_meme()
    print('finished!')
    return 'finished!',200


'''gui in browser'''
@app.route('/findmemes')
def find_meme_gui():
    return render_template('gui.html')
@io.on('connect')
def on_connect():
    print('socket connected!')
@io.on('disconnect')
def on_disconnect():
    print('socket disconnected!')
@io.on('find_meme')
def on_find_meme(msg):
    print('socket received:',msg)
    meme_text=msg['data']
    MemeSOCKET(meme_text,socket=io,session_id=request.sid).send_meme()
    emit('system_msg',{'data':'loading.......'})

#only for check
@app.route('/')
def home():
    return 'fine',200

#test
@app.route('/start_task')
def start_task():
    def sleep():
        import time
        time.sleep(20)
        print('done')

    thread = Thread(target=sleep)
    thread.start()
    return 'started'

