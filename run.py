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
    print(request.values)
    """Respond to incoming texts with a text from your bot"""
    request_message = request.values.get('Body','Hi')
    full_bot_response = api.talk(user_key, app_id, host, botname, request_message, session_id=True, trace=True)
    '''parse response'''
    bot_response = full_bot_response["response"]
    session_response = full_bot_response["sessionid"]

    # debug = api.debug_bot(user_key, app_id, host, botname, request_message, session_id=True, reset=False, trace=True, recent=True)
    print(full_bot_response)


    soup = BeautifulSoup(bot_response, "lxml")
    partition = bot_response.partition('<img')
    text_portion = partition[0]
    #image_portion = soup.img.extract()['src']

    # construct response
    resp = twilio.twiml.Response()

    '''text response'''
    #broken up responses
    # for i,v in enumerate(text_portion.rsplit("\n")):
    # 	print(i)
    # 	resp.message(msg=text_portion.rsplit("\n")[i])

    #fat responses
    resp.message(msg=text_portion)

    '''image response'''
    # resp.message().media(image_portion)
    print(resp)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)