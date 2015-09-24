from flask import Flask, request, redirect, make_response, session
import twilio.twiml
from pb_py import main as api
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import requests
from zenpy import Zenpy
import json
# from celery import Celery


host = 'aiaas.pandorabots.com'
user_key = '8704f84cef67d2c4c1c487ce9aab7da2'
app_id = '1409612152298'
botname = 'benjamin'
app = Flask(__name__)
app.secret_key="\xae\xfb\x10\xaa\x06l\x91\xaeg\xb3z\xa9j\x92\xcc\x08)\xa2\x1e\x9aw9\xf8%"

zenpy = Zenpy('textbenjamin', 'daniel@textbenjamin.com', 'SoC5ZLSVqnJHAUd2ABJj7AnEsqMeZqKHurrHV5Ij')

user = 'daniel@textbenjamin.com'
pwd = 'boris5423'


@app.route("/", methods=['GET','POST'])
def bot_talk():
    
    """Respond to incoming texts with a text from your bot"""
    print "request url"
    print request.url
    # find user
    # if users exists, find ticket, and add comment to ticket
    # else, create new ticket for user and user implicitly
    request_message = request.values.get('Body','Hi')
    phone = request.values.get('From','+11111111111')

    # lookup whether this user is in zendesk
    possible_existing_user = zenpy.search(type='user', phone=phone)

    if possible_existing_user:

        # lookup the ticket belonging to this user
        relevant_ticket = zenpy.search(type='ticket', requester_id = possible_existing_user.next().id).next()

        ## prepare update ticket request
        # set url
        url = 'https://textbenjamin.zendesk.com/api/v2/tickets/' + str(relevant_ticket.id) + '.json'

        #set data 
        data = {
                    "ticket": {
                        "comment":{ 
                            "body": request_message
                        }
                    }
                }

        # set headers
        headers = {'content-type': 'application/json'}

        # make request
        updated_ticket_response = requests.put(url, data = json.dumps(data), auth=(user, pwd), headers=headers)
  

    else:

        ## prepare request to create ticket for this user
        #set url
        url = 'https://textbenjamin.zendesk.com/api/v2/tickets.json'

        #set data 
        data = {
                    "ticket": {
                        "requester": {
                            "name" : phone,
                            "phone": phone
                            },
                        "comment":{ 
                            "body": request_message
                        },
                        "subject": 'Request'
                    }
                }

        # set headers
        headers = {'content-type': 'application/json'}

        # make request to create ticket
        createTicketResponse = requests.post(url, data=json.dumps(data), auth=(user, pwd), headers=headers)

        
        



    #gets request body, default body to hi if it is emptpy
    

    # calls the atalk endpoint with session_id and client_name is they exists in the session, otherwise without them
    if session.get('session_id') != None or session.get('client_name') != None:
        session_id = session.get('session_id')
        client_name = session.get('client_name')
        query = "https://aiaas.pandorabots.com/atalk/" + str(app_id) + "/" + str(botname) + "?user_key=" + str(user_key) + "&input=" + str(request_message) + '&client_name=' + str(client_name) + '&sessionid=' + str(session_id)
        

    else:
        query = "https://aiaas.pandorabots.com/atalk/" + str(app_id) + "/" + str(botname) + "?user_key=" + str(user_key) + "&input=" + str(request_message)

    #parsing the response into json
    r=requests.post(query)
    full_bot_response = r.json()
    bot_response = full_bot_response["responses"][0]


    #setting session values
    session['session_id'] = full_bot_response['sessionid']
    session['client_name'] = full_bot_response['client_name']
    
 

    # parsing out image urls from the message
    soup = BeautifulSoup(bot_response, "lxml")
    partition = bot_response.partition('<img')
    text_portion = partition[0]
    #image_portion = soup.img.extract()['src']

    # construct twiml response
    resp = twilio.twiml.Response()




    '''text response'''
   
    resp.message(msg=text_portion)

    '''image response'''
    # resp.message().media(image_portion)
    # return main_resp
    return str(resp)
    



if __name__ == "__main__":
    app.run(debug=True)