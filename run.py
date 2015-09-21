from flask import Flask, request, redirect
import twilio.twiml
from pb_py import main as api
from bs4 import BeautifulSoup

host = 'aiaas.pandorabots.com'
user_key = '8704f84cef67d2c4c1c487ce9aab7da2'
app_id = '1409612152298'
botname = 'benjamin'

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def bot_talk():
    """Respond to incoming texts with a text from your bot"""
    request_message = request.values.get('Body',  'Hi')
    bot_response = api.talk(user_key, app_id, host, botname, request_message)["response"]
    '''parse response'''
    soup = BeautifulSoup(bot_response, "lxml")
    partition = bot_response.partition('<img')
    text_portion = partition[0]
    #image_portion = soup.img.extract()['src']

    # construct response
    resp = twilio.twiml.Response()

    '''text response'''

    for i,v in enumerate(text_portion.rsplit("\n")):
    	print(i)
    	resp.message(msg=text_portion.rsplit("\n")[i])


    '''image response'''
    # resp.message().media(image_portion)
    # print(resp)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)