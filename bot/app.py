from pymessenger.bot import Bot
from flask import Flask,request
import os
import json
from .spongebob_memes import find_meme,SearchQueryNotValidError

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
        for message in entry.get('messaging'):
            if message.get('message'):
                sender_id = message['sender']['id']
                recipient_id = message['recipient']['id']
                if msg_text:=message['message'].get('text'):
                    print('get text:',msg_text)
                    if msg_text=="ㄛㄛ":
                        bot.send_text_message(sender_id,msg_text)
                        continue
                    try:
                        meme_url=find_meme(msg_text)
                    except SearchQueryNotValidError as e:
                        print(e.__class__,":",e)
                        meme_url=None
                    if meme_url:
                        print(f'found meme at {meme_url}')
                        bot.send_image_url(sender_id,meme_url)
                    else:
                        print('meme not found!')
    print('finished!')
    return 'finished!',200

#only for check
@app.route('/')
def home():
    return 'fine',200