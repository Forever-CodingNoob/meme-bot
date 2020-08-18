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

@app.route('/callback',methods=('POST',))
def verify():
    print('query strings:',request.args)
    return 'hola'


#only for check
@app.route('/')
def home():
    return 'fine',200