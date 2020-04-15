# from https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# see https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/

# to do: use ngrok as a webhook (to push updates to our server) 
# instead of constantly polling API (aka pulling; this is not an efficient use of computing power)
# https://sendgrid.com/blog/whats-webhook/
# https://core.telegram.org/bots/webhooks

## TELEGRAM BOT IMPORTS ##
import json, requests, time
from datetime import datetime, timedelta

## FLASK IMPORTS ##
from flask_cors import CORS 
from flask import Flask, request, jsonify
import subprocess
from os import environ

import pytz

# from flask_sqlalchemy import SQLAlchemy

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

def get_updates():
    """(returns: dictionary) Get JSON of messages sent to bot."""
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js

def send_message(text, chat_id):
    """Send a message to a specific chat id."""
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

## receiver function
# Al's chat id is 525217801
# Zen's id is 254774472
# Bryan's id is 32738303
@app.route("/message/<string:chatId>", methods = ['POST'])
def send(chatId):
    """Send a message to the chatId in the url. Takes in a json { message : message_body }, ignoring content type"""
    # ensure chatId is a number
    try:
        int(chatId)
    except:
        print("Chat ID is invalid!")
        # raise("Chat ID is invalid!")

    # today = datetime.now().date()
    print("[!] Message sending...")

    # Receive the message from the posted json 
    # We assume the JSON format will be {message : message_content}
    jsonOut = request.get_json(force = True) # ignore content type
    message = jsonOut['message']
    print(timestamp() + ' - "' + message + '"' + " sent to user with chat ID " + str(chatId)) # debugging

    # Send message to a specific chat id
    send_message(message, chatId)

    return "Success!"

# @app.route("/sendImage/<string:chatId>", methods = ['POST'])
# def sendImage(chatId, imageFile):
#     # need to get imageFile
#     command = 'curl -s -X POST https://api.telegram.org/bot' + TOKEN + '/sendPhoto -F chat_id=' + chatId + " -F photo=@" + imageFile
#     subprocess.call(command.split(' '))
#     return
def get_ngrok_url():

    url = environ.get('ngrok_url', "http://localhost:4040/api/tunnels") 
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]

@app.route("/receiveUrl/<string:routing_id>")
def receiveUrl(routing_id):
    try:
        telegram_poll_url = environ.get('telegram_poll_url',"http://localhost:8990/")
        r_telegram_poll = requests.get(f"{telegram_poll_url}getUserChatId/driver")
        driver_chat_id = int(r_telegram_poll.text)
        try:
            ngrok_url = get_ngrok_url()
            toSend = f"{ngrok_url}/{routing_id}"
            send_message(toSend, chat_id=driver_chat_id)
            return toSend
        except:
            # if ngrok doesnt work
            url = "http://localhost:5006/"
            toSend = "ngrok does not work when connected to SMU wifi. Please connect to a non-SMU wifi to test"
            send_message(toSend, chat_id=driver_chat_id)
            return toSend
    except:
        pass
    

    

# run code
if __name__ == '__main__':
    app.run(host="0.0.0.0",port = 8989, debug = True) # turn this OFF for production!