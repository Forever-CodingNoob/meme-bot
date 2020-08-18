from pymessenger.bot import Bot
from flask import Flask,request
import os
import json
from .spongebob_memes import find_meme

'''load secret tokens(.env file is not uploaded for preventing revealing the secret tokens inside, hence setting environment variables on cloud platform is a must):
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.abspath(__file__),'..\\..\\.env'))
'''

PAGE_ACCESS_TOKEN=os.environ['PAGE_ACCESS_TOKEN']
VERIFICATION_TOKEN=os.environ['VERIFICATION_TOKEN']

app=Flask(__name__)
bot=Bot(PAGE_ACCESS_TOKEN)

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
        for messaging in entry.get('messaging'):
            sender_id = messaging['sender']['id']
            recipient_id = messaging['recipient']['id']
            if msg:=messaging.get('message'):
                if msg_text:=msg.find('text'):
                    print('get text:',msg_text)
                    meme_url=find_meme(msg_text)
                    if meme_url:
                        print(f'found meme at {meme_url}')
                        bot.send_image_url(recipient_id,meme_url)
                    else:
                        print('meme not found!')
    return 'finished!',200

#only for check
@app.route('/')
def home():
    return 'fine',200