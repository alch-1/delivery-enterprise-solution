# Takes in a json at http://127.0.0.1:5000/purchase 
# with JSON variables customer_name, telehandle, address, postal_code, quantity, 
# purchase_amount, date_of_delivery, timeslot
# 
# 
import sys
import os
import json, requests, time
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import pika
import uuid
from os import environ

import pytz

app = Flask(__name__)

app.config["SQLALCHEMY_BINDS"] = {
    'sql_order': environ.get('order_db_url', "mysql+mysqlconnector://root@localhost:3306/order"),
}

# connect to order
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/Order' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Telegram config
# ADMIN_CHAT_ID = "170598495"
# telegram bot listener is running on a flask program
TELEGRAM_URL = environ.get("telegram_url","http://127.0.0.1:8989/message/")

# Payment API config
# PAYMENT_URL = "http://127.0.0.1:5002/payment/create"

# allow cross origin resource sharing
CORS(app)

## TELEGRAM BOT FUNCTIONS ##
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
        return timestamp() + " Can't make request: " + e
    
    content = response.content.decode("utf8")
    return content

def send_message(text, chat_id):
    """Send a message to a specific chat id."""
    url = TELEGRAM_URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

## DATABASE CLASSES ##
db = SQLAlchemy(app)

class Order(db.Model):
    __bind_key__ = 'sql_order'
    __tablename__ = 'order'
    

    # customer_name = db.Column(db.String(64), nullable = False)
    order_id = db.Column(db.Integer, primary_key=True)
    telehandle = db.Column(db.String(64), nullable = False)
    transaction_id = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(200), nullable = False)
    postal_code = db.Column(db.String(200), nullable = False)
    purchase_amount = db.Column(db.Float(precision = 2), nullable = False)
    date_of_delivery = db.Column(db.Date())
    timeslot = db.Column(db.String(2))
    ts = db.Column(db.DateTime()) 

    # Individual items
    product_name = db.Column(db.String(64))
    product_id = db.Column(db.Integer())
    unit_price = db.Column(db.Float(precision = 2))
    quantity = db.Column(db.Integer())

    def __init__(self, telehandle, transaction_id, address, postal_code, purchase_amount, date_of_delivery, timeslot, product_name, product_id, unit_price, quantity):
        # self.customer_name = customer_name
        self.telehandle = telehandle
        self.address = address
        self.transaction_id = transaction_id
        self.postal_code = postal_code
        self.quantity = quantity
        self.purchase_amount = purchase_amount
        self.date_of_delivery = date_of_delivery
        self.timeslot = timeslot
        # self.ts = ts
        self.product_name = product_name
        self.product_id = product_id
        self.unit_price = unit_price
        self.quantity = quantity

    def json(self):
        return {
            # "CustomerName": self.customer_name, 
            "Telehandle":self.telehandle, 
            "OrderId":self.order_id, 
            "TransactionId":self.transaction_id, 
            "Address":self.address,
            "PostalCode":self.postal_code, 
            "Product": self.product_name,
            "Quantity":self.quantity,
            "PurchaseAmount":self.purchase_amount,
            "DateOfDelivery":self.date_of_delivery,
            "Timeslot":self.timeslot,
            "Timestamp":self.ts
        }

@app.route("/view_orders")
def get_all():
    return jsonify({"Orders" : [order.json() for order in Order.query.all()]})

@app.route("/order/<int:order_id_input>")
def find_by_orderid(order_id_input):
    order = Order.query.filter(Order.product_name.contains(order_id_input)).all()
    try:
        if order:
            return jsonify({"Order":[order.json() for order in order]}), 201
        return jsonify({"message":"Order not found."}),201
    except:
        return jsonify({"message":"error occur while querying database"}), 404

# @app.route("/order/<string:order_id_input>",methods=['POST'])
def create_order(order_id_input):
    if (Order.query.filter_by(order_id=order_id_input).first()):
        return jsonify({"message": "A order with Order ID '{}' already exists".format(order_id_input)}),400

    data = request.get_json()

    order = Order(order_id_input, **data)

    try:
        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({"message":"An error occured creating the order."}),500

    return jsonify(order.json()),201

@app.route("/purchase/<string:product_id>", methods=['POST'])
def create_product(product_id):
    if (Order.query.filter_by(product_id=product_id).first()):
        return jsonify({"message": "A furniture with productID '{}' already exists".format(product_id)}),400
        
    data = request.get_json()

    furniture = Furniture(product_id, **data)

    try:
        db.session.add(furniture)
        db.session.commit()
    except:
        return jsonify({"message":"An error occured creating the furniture."}),500

    return jsonify(furniture.json()), 201

## HANDLE PURCHASES ##
@app.route("/purchase", methods=['POST']) # take in a JSON
def purchase():
    print("[!] Receiving purchase...")
    
    try:
        jsonIn = request.get_json(force = True) # this is a string when sent via browser
        print(type(jsonIn))
        print(jsonIn)
        # return "No" 
    except requests.exceptions.RequestException:
        return jsonify(message="An error occured while receiving the order information! " + str(e),status=400)
    data = json.loads(jsonIn)
    # data = jsonIn
    # print

    transaction_id = data['payment_id']
    corrid = data['corrid']
    
    purchase_details = receivePurchase(corrid)
    print(purchase_details)
    
    telehandle = purchase_details["telehandle"]
    address = purchase_details["address"]
    postal_code = purchase_details["postal_code"]
    date_of_delivery = purchase_details["date_of_delivery"]
    timeslot = purchase_details["timeslot"]
    total_price = purchase_details["total_price"]

    cart_details = purchase_details['cart_details']
    print(cart_details)
    for product in cart_details:
        print(product)
        order_obj = Order(
            telehandle,
            transaction_id,
            address,
            postal_code,
            total_price,
            date_of_delivery,
            timeslot,
            product['product_name'],
            product['product_id'],
            product['price'],
            product['quantity']
        )

        try:
            print(order_obj)
            db.session.add(order_obj)
            db.session.commit()
            print("[i] Order added to database")
        except Exception as e:
            print(str(e))
            return jsonify({"message":"An error occured creating the order! " + str(e)}), 400
        
        ## Send post to furniture.py to decrement ##
        try:
            product_url = environ.get('product_url', "http://127.0.0.1:5003/")
            # print(product['product']) # debugging
            r_furniture = requests.post(product_url + "decrease/" + str(product['product_id']) + "/" + str(product['quantity']))
        except requests.exceptions.RequestException as e:
            print(str(e))
            return jsonify({"message":"Error while posting to furniture.py! " + str(e)}), 400
        print("[i] Decrement request sent to furniture.py")

        ## Send notification to store admin via telegram ##
        # make a dict and convert to json
        telegramData = r'{"message": "' + str(timestamp()) + " An order for " + product['product_name'] + " has been placed by " + telehandle + r'"}'
        # send json data to the telegram url using post 
        try:
            telegram_poll_url = environ.get('telegram_poll_url',"http://localhost:8990/")
            r_telegram_poll = requests.get(f"{telegram_poll_url}getUserChatId/admin")
            admin_chat_id = r_telegram_poll.text
            if admin_chat_id != "":
                send_url = TELEGRAM_URL + admin_chat_id
                try:
                    r_telegram = requests.post(send_url, data = telegramData)
                    print("[i] Message request sent to telegramBot.py")
                except requests.exceptions.RequestException as e:  
                    print(str(e))
                    return jsonify(message="Error while posting to telegramBot.py! " + str(e), status = 400)               
        except:
            pass
        

    # success
    return jsonify({"message": "success"}), 201

@app.route("/getRoute/<string:timeslot>")
def getByTimeslot(timeslot): 
    """ Takes in a timeslot, returns a json of deliveries for that timeslot """
    today = datetime.now().strftime('%Y-%m-%d')
    if timeslot == 'AM':
        order = Order.query.filter(Order.timeslot.contains('AM')).filter(Order.date_of_delivery.contains(today)).all()
    elif timeslot == 'PM':
        order = Order.query.filter(Order.timeslot.contains('PM')).filter(Order.date_of_delivery.contains(today)).all()
    try:
        if order: # order is a list of Order objects
            toSend = {"delivery": []} # empty dictionary
            for order in order:
                d = order.json() # dictionary of order details
                # print(d)
                print(d.get("OrderId"), d.get("Telehandle"), d.get("Timeslot"), d.get("DateOfDelivery"))
                toSend.get("delivery").append({"order_id": d.get("OrderId"), "telehandle": d.get("Telehandle"), "timeslot": d.get("Timeslot"), "date" : d.get("DateOfDelivery").strftime("%Y-%m-%d"), "product": d.get('Product'), "quantity": d.get('Quantity')})
            
            try:
                routing_url = environ.get('routing_url', "http://127.0.0.1:5006/")
                r = requests.post(url = f"{routing_url}processRoute", json=json.dumps(toSend))
                print("[i] Sent post request to processRoute")
            except requests.exceptions.RequestException as e:
                print(str(e))
                return jsonify(message="Error while posting to processRoute on port 5006! " + str(e), status = 400)
            return jsonify(toSend), 201
        return jsonify({"message":"Order not found."}),201
    except:
        return jsonify({"message":"error occur while querying database"}), 404


def receivePurchase(corrid):
    rabbit_host = environ.get('rabbit_host', 'localhost') # default host
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=port))
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="payment_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct', durable=True)

    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue='payment', durable=True) # '' indicates a random unique queue name; 'exclusive' indicates the queue is used only by this receiver and will be deleted if the receiver disconnects.
        # If no need durability of the messages, no need durable queues, and can use such temp random queues.
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='payment.detail') # bind the queue to the exchange via the key
        # Can bind the same queue to the same exchange via different keys

    # set up a consumer and start to wait for coming messages, stop upon 5 seconds of inactivity
    results = []
    for method, properties, body in channel.consume(queue=queue_name, inactivity_timeout=5):
        if body == None:
            print("no more message")
            break
        
        # Acknowledge the message
        channel.basic_ack(method.delivery_tag)
        if properties.correlation_id == corrid:
            data = json.loads(body)
            break
        else:
            channel.basic_publish(exchange=exchangename, routing_key="payment.detail", body=body,
                properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
                    correlation_id=properties.correlation_id # set the correlation id for easier matching of replies
                )
            )

    connection.close()

    return data


## Run flask ##
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug = True)