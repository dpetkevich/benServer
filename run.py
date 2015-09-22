from flask import Flask, request, redirect, make_response, session
import twilio.twiml
from pb_py import main as api
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

host = 'aiaas.pandorabots.com'
user_key = '8704f84cef67d2c4c1c487ce9aab7da2'
app_id = '1409612152298'
botname = 'benjamin'
app = Flask(__name__)
app.secret_key="\xae\xfb\x10\xaa\x06l\x91\xaeg\xb3z\xa9j\x92\xcc\x08)\xa2\x1e\x9aw9\xf8%"


@app.route("/", methods=['GET','POST'])
def bot_talk():
    print(request.values)
    print(session.get('session_id'))
    """Respond to incoming texts with a text from your bot"""

    request_message = request.values.get('Body','Hi')
   

    if session.get('session_id') != None:
        session_id = session.get('session_id')
        client_name = session_id
        print('in if')
        print(session_id)
        full_bot_response = api.talk(user_key, app_id, host, botname, request_message, session_id, client_name, trace=True)
    else:
        full_bot_response = api.talk(user_key, app_id, host, botname, request_message, trace=True)
        session_id = full_bot_response["sessionid"]


    '''parse response'''
    bot_response = full_bot_response["response"]

    print(full_bot_response)


    soup = BeautifulSoup(bot_response, "lxml")
    partition = bot_response.partition('<img')
    text_portion = partition[0]
    #image_portion = soup.img.extract()['src']

    # construct twiml response
    resp = twilio.twiml.Response()

   
    session['session_id'] = session_id
    session['client_name'] = client_name

    '''text response'''
    #broken up responses
    # for i,v in enumerate(text_portion.rsplit("\n")):
    # 	print(i)
    # 	resp.message(msg=text_portion.rsplit("\n")[i])

    #fat responses
    resp.message(msg=text_portion)

    '''image response'''
    # resp.message().media(image_portion)
    print(str(resp))
    return str(resp)
    # return main_resp

if __name__ == "__main__":
    app.run(debug=True)