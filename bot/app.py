from pymessenger.bot import Bot
from flask import Flask,request
import os

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
    print('query strings:',request.args)
    if request.args.get('hub.mode')=='subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token')==VERIFICATION_TOKEN:
            return request.args["hub.challenge"], 200
        return 'verification_token mismatch!',403
    return 'hola',200


#only for check
@app.route('/')
def home():
    return 'fine',200