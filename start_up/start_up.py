from os import environ
import requests
import time

routing_url = environ.get('routing_url', 'http://localhost:5006/')
telegram_poll_url = environ.get('telegram_poll_url', 'http://localhost:8990/')

while True:
    try:
        r_routing = requests.get(routing_url)
        r_telegram_poll = requests.get(telegram_poll_url)
        print(r_routing.text, r_telegram_poll.text)
        break
    except:
        print('service not up yet')
        time.sleep(5)
