# from https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# see https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/

# to do: use ngrok as a webhook (to push updates to our server) 
# instead of constantly polling API (aka pulling; this is not an efficient use of computing power)
# https://sendgrid.com/blog/whats-webhook/
# https://core.telegram.org/bots/webhooks

## TELEGRAM BOT IMPORTS ##
import json, requests, time
from datetime import datetime, timedelta

## COMMUNICATION IMPORTS ##
# Use a message-broker with 'direct' exchange to enable interaction
import pika, uuid
from os import environ

## FLASK IMPORTS ##
from flask_cors import CORS 
from flask import Flask, request, jsonify
import subprocess

from flask_sqlalchemy import SQLAlchemy

from apscheduler.schedulers.background import BackgroundScheduler

import pytz

app = Flask(__name__) # new flask app
CORS(app) # not sure if this is needed 

###### BOT MAIN CODE ######
BOT_INFO = """ 
Done! Congratulations on your new bot. You will find it at t.me/FurnitureMessengerBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
1086413321:AAHlEl_bS2NiAbJF_ppgW9J4pJw7S-588jI
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
"""
###########################

# {!} Explanation of libraries: 
# requests: make requests
# json: parses JSON files (telegram's API returns JSONs)
# time: sleep between json fetches
# datetime: get today's date

# do NOT upload this token to publicly available websites, it allows anyone to intercept your messages.
TOKEN = r"1229382631:AAE9DnrCqai9hgC4IicESFikjZxcRpsOoF0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('telegram_db_url','mysql+mysqlconnector://root@localhost:3306/telegramdata')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db = SQLAlchemy(app)

class TelegramData(db.Model):
    __tablename__ = 'telegramdata'

    telehandle = db.Column(db.String(64), primary_key = True)
    chat_id = db.Column(db.Integer, nullable = False)
    user_type = db.Column(db.String(64), nullable = False)


    def __init__(self, chat_id, telehandle, user_type):
        self.telehandle = telehandle
        self.chat_id = chat_id
        self.user_type = user_type

    def json(self):
        return {"telehandle":self.telehandle, "chat_id":self.chat_id, "user_type": self.user_type}

@app.route("/")
def start_up():
    return "Started"

def update_database(chat_id, telehandle, user_type = 'customer'):
    telehandle = "@"+telehandle
    telegram_data = TelegramData.query.filter_by(telehandle = telehandle).first()
    if telegram_data:
        if user_type == 'driver':
            telegram_data.user_type = user_type
            try:
                db.session.commit()
            except:
                return "Error in updating record"
        elif user_type == 'admin':
            telegram_data.user_type = user_type
            try:
                db.session.commit()
            except:
                return "Error in updating record"
        return telegram_data
    else:
        tele_obj = TelegramData(chat_id,telehandle,user_type)
        try:
            db.session.add(tele_obj)
            db.session.commit()
            return tele_obj
        except:
            return "Error in adding record"

@app.route("/getChatId/<string:telehandle>")
def get_tele_chat_id(telehandle):
    telegram_data = TelegramData.query.filter_by(telehandle = telehandle).first()
    if telegram_data:
        print("chat_id", telegram_data.chat_id)
        return str(telegram_data.chat_id)
    return ''

@app.route("/getUserChatId/<string:user_type>")
def get_user_tele_chat_id(user_type):
    telegram_data = TelegramData.query.filter_by(user_type = user_type).first()
    if telegram_data:
        print("chat_id", telegram_data.chat_id)
        return str(telegram_data.chat_id)
    return ''

def timestamp():
    """Return timestamp"""
    ts = datetime.now(tz=pytz.timezone('Asia/Singapore'))
    st = ts.strftime('%d-%m-%Y [ %I:%M %p ]')
    return st

def get_url(url):
    """(returns: string) Get content from given URL. Uses GET"""
    try:
        response = requests.get(url)
    except Exception as e:
        return timestamp() + " Can't make request: " + str(e)
    
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    """(returns: dictionary) Get JSON from given URL."""
    content = get_url(url)
    js = json.loads(content) # loads <=> load string
    return js

def get_updates(url = URL):
    """(returns: dictionary) Get JSON of messages sent to bot."""
    updateUrl = url + "getUpdates"
    js = get_json_from_url(updateUrl)
    return js

def get_last_chat_id_and_text(updates):
    """(returns: tuple) Return text and chat id of last sent message."""
    # updates["result"] is a list of dictionaries
    num_updates = len(updates["result"])
    if num_updates > 0:    
        index = num_updates - 1  # gets the index of the last dictionary entry
        last_update = updates["result"][index]
        print(last_update)
        # get the text of the last sent message
        text = last_update["message"]["text"]
        message_id = last_update['message']['message_id']
        # get the chat id of the last sent message
        chat_id = last_update["message"]["from"]["id"]

        # get first name
        first_name = last_update["message"]["from"]["first_name"]

        try:
            username = last_update['message']["from"]['username']
        except KeyError:
            username = ""
        
        # get last name if it exists
        try: 
            last_name = last_update["message"]["from"]["last_name"]
        except KeyError:
            # Don't need logging, this is not vital. Last names are not compulsory
            last_name = ""
        name = first_name + " " + last_name
        return (str(message_id), text, chat_id, name, username)
    else:
        return (None, None, None, None, None)

def get_telehandle(order_id, routing_id):
    routing_url = environ.get("routing_url", "http://127.0.0.1:5006/")
    send_url = f"{routing_url}telehandle/{order_id}/{routing_id}"

    try:
        r = requests.get(send_url)
        print("telehandle", r.text)
        return r.text
    except requests.exceptions.RequestException as e:
        print(str(e))

def get_routing_status(order_id):
    routing_url = environ.get("routing_url", "http://127.0.0.1:5006/")
    send_url = f"{routing_url}route_details/{order_id}"

    try:
        r = requests.get(send_url)
        result = eval(r.text)
        if result['order_id']:
            return result['delivery_status']
    except requests.exceptions.RequestException as e:
        print(str(e))

def schedule(): # sleep in seconds 
    
    telegram_url = environ.get('telegram_url', "http://127.0.0.1:8989/message/")
    customerURL = telegram_url
    # Al's chat id is 525217801
    # Zen's id is 254774472
    # Bryan's id is 32738303

    print("[!] Telegram Polling Service started on", timestamp(), "polling", URL)
    last_seen_id = environ.get('last_seen_id', '')

    updates = get_updates()
    message_id, text, chat_id, name, username = get_last_chat_id_and_text(updates)
    
    if ((text, chat_id, name) != (None, None, None)) & (message_id != last_seen_id) & (last_seen_id != ""): 
        print(username)
        print(f"From: {name} ({chat_id})")
        print("Received text: " + text)
        last_seen_id = message_id
        environ['last_seen_id'] = message_id
        

        telegram_user = update_database(chat_id, username)
        if 'driver' in text:
            telegram_user = update_database(telegram_user.chat_id, telegram_user.telehandle[1:], 'driver')
        elif 'admin' in text:
            telegram_user = update_database(telegram_user.chat_id, telegram_user.telehandle[1:], 'admin')
        elif "Start" in text and telegram_user.user_type == 'driver': # sample input: "Start AM"
            # get routes
            timeslot = text.split(" ")[1]
            # get purchases from purchase db, send to routing.py
            purchase_url = environ.get('purchase_url', "http://127.0.0.1:5001/")
            if timeslot == "AM":
                print("Sending data for AM")
                r = requests.get(purchase_url + "getRoute/AM")
            elif timeslot == "PM":
                print("Sending data for PM")
                r = requests.get(purchase_url + "getRoute/PM") 
            else:
                print("Invalid input!")
        # elif "End" in text: # may be redundant 
        #     # end delivery
        #     pass
        elif "OK" in text and telegram_user.user_type == 'driver': # delivery done; sample input: "<routing_id><order_id> OK"
            code = text.split(" ")[0]

            routing_id = code.split('-')[0]
            order_id = code.split('-')[1]
            print("Sending data to indicate delivery is done")

            delivery_status = get_routing_status(order_id)
            # print(delivery_status)
            if delivery_status != "Completed":
                ## AMQP START ##
                # default username / password to the borker are both 'guest'
                rabbit_host = environ.get('rabbit_host', 'localhost')
                # default broker hostname. Web management interface default at http://localhost:15672
                port = 5672 # default messaging port.
                # connect to the broker and set up a communication channel in the connection
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=port))
                    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
                    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
                channel = connection.channel()

                # set up the exchange if the exchange doesn't exist
                exchangename="route_direct"
                channel.exchange_declare(exchange=exchangename, exchange_type='direct', durable=True)
                
                # prepare the message body content
                message = json.dumps({'routing_id': routing_id, 'order_id' : order_id, 'delivery_status': 'Completed'})
                
                
                # Prepare the correlation id and reply_to queue and do some record keeping
                corrid = str(uuid.uuid4())
                # prepare the channel and send a message to Shipping
                channelqueue = channel.queue_declare(queue='routing.update', durable=True) # make sure the queue used by Shipping exist and durable
                queue_name = channelqueue.method.queue
                channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='routing.update') # make sure the queue is bound to the exchange
                channel.basic_publish(exchange=exchangename, routing_key="routing.update", body=message,
                    properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
                        correlation_id=corrid # set the correlation id for easier matching of replies
                    )
                )
                print("Sent data to indicate delivery is done - code: " + routing_id + order_id)

                # close the connection to the broker
                connection.close()

                # send to customer that delivery is done:
                try:
                    telegramData = json.dumps({"message": f"{timestamp()} Your order no. {routing_id}-{order_id} has arrived!"})
                    telehandle = get_telehandle(order_id, routing_id)
                    customer_chat_id = get_tele_chat_id(telehandle)
                    print("chat_id", customer_chat_id)
                    
                    sent_url = customerURL + str(customer_chat_id)
                    r = requests.post(sent_url, data = telegramData)
                    print("Sending delivery notification to customer")
                except requests.exceptions.RequestException as e:  
                    print("Error while posting to telegramBot.py! " + str(e))
            
            # r = requests.post()
            # TODO send data to routing.py to mark the delivery as done
        else:
            print(timestamp(), "Invalid text sent!")
    else:
        print('no new text')
        last_seen_id = message_id
        environ['last_seen_id'] = message_id

@app.before_first_request
def before_first_request():
    if not app.debug or environ.get("WERKZEUG_RUN_MAIN") == "true":
        sched = BackgroundScheduler()
        sched.add_job(schedule, 'interval', seconds=3)
        sched.start()

if __name__ == '__main__':
    app.run(port=8990, host='0.0.0.0')

    

