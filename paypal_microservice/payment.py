from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# import traceback
import paypalrestsdk
import requests

import pika
import json
import uuid
from os import environ

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('paypal_db_url', "mysql+mysqlconnector://root@localhost:3306/paypal")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.String(100), primary_key=True)
    recipent_email = db.Column(db.String(100), nullable=False)
    net_amount = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(30), nullable = False)

    def __init__(self, id, recipent_email, net_amount, address, status):
        self.id = id
        self.recipent_email = recipent_email
        self.net_amount = net_amount
        self.status = status

    def json(self):
        return {"id": self.id, "recipent_email": self.recipent_email, "net_amount": self.net_amount, "address": self.address, "status": self.status}


@app.route("/payment/create", methods = ['POST'])
def create_payment():
    access_token()
    return_url = "http://localhost:5002/payment/execute"
    cancel_url = "http://localhost/esd-project/Refurban/"
    
    try:
        data = request.get_json(force = True)
    except Exception as e:
        print(e)

    amount = data['amount']
    purchase_details = json.dumps(data['purchase_details'])
    
    corrid = str(uuid.uuid4())
    sendPurchase(purchase_details, corrid)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [
            {
                "amount": amount,
                "description": corrid
            }
        ]
    })
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return jsonify({"approval_url": approval_url}), 201
    else:
        return jsonify({"message": payment.error}), 400

@app.route("/payment/execute")
def execute_payment():
    access_token()

    args = request.args

    paymentId = args.get('paymentId')
    payer_id = args.get('PayerID')
    payment = paypalrestsdk.Payment.find(paymentId)
    if payment.execute({"payer_id": payer_id}):
        payment_details = get_payment_details(payment)

        corrid = payment.transactions[0]["description"]
        
        transaction_obj = Transaction(**payment_details)
        try:
            db.session.add(transaction_obj)
            db.session.commit()
            
            transaction_details = {
                'payment_id' : paymentId,
                'corrid' : corrid
            }
            
            purchase_url = environ.get('purchase_url', "http://localhost:5001/purchase")
            try:
                r_purchase = requests.post(purchase_url, json=json.dumps(transaction_details))
                # return redirect("http://localhost:8000/index.php?alert=Thank you for making a purchase with us!", code=302)
                if r_purchase.status_code == 201:
                    return redirect("http://localhost:8000/index.php?modal=show", code=302)
                else:
                    return "error", 400
            except:
                return purchase_url, 500
            
        except:
            return jsonify({"message": "An error occurred creating the transaction."}), 500
        
        
    else:
        return jsonify({"message": payment.error}), 400 # Error Hash

def access_token():
    paypalrestsdk.configure({
        "mode": "sandbox", # sandbox or live
        "client_id": "AYvQXXc8D0tQMsPukuxIGp7my9zy1p84DemafShdmneOymvKH5gPxPZfQuB2CStUOrWdN1-_RPh9HTbN",
        "client_secret": "EMm-T_Ts77ncqjT4W0NpcHD_17cSdd1TvRwmq6r64hr5sVrIePsPbJJHassc9aXG4JcA9ekzgoFtRy_a" 
    })

def get_payment_details(payment):
    id = payment.id
    status = payment.payer.status
    recipent_email = payment.payer.payer_info.email
    address = payment.payer.payer_info.shipping_address.line1
    postal_code = payment.payer.payer_info.shipping_address.postal_code
    net_amount = payment.transactions[0].amount.total

    details = {
        "id": f"{id}",
        "recipent_email": f"{recipent_email}",
        "net_amount": f"{net_amount}",
        "address": f"{address}, S{postal_code}",
        "status": f"{status}"
    }
    return details


def sendPurchase(purchase_details, corrid):
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
    exchangename="payment_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct', durable=True)
    # prepare the message body content
    message = purchase_details # convert a JSON object to a string

    # Prepare the correlation id and reply_to queue and do some record keeping
    
    # prepare the channel and send a message to Shipping
    channelqueue = channel.queue_declare(queue='payment', durable=True) # make sure the queue used by Shipping exist and durable
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='payment.detail') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="payment.detail", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            correlation_id=corrid # set the correlation id for easier matching of replies
        )
    )

    # close the connection to the broker
    connection.close()
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)