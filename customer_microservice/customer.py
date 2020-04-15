from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('customer_db_url','mysql+mysqlconnector://root@localhost:3306/customer')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    telehandle = db.Column(db.String(64), primary_key = True)
    address = db.Column(db.String(200), nullable = False)
    postal_code = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(64), nullable = False)


    def __init__(self, telehandle, address, postal_code, password):
        self.telehandle = telehandle
        self.address = address
        self.postal_code = postal_code
        self.password = password

    def json(self):
        return {"telehandle":self.telehandle, "address":self.address, "postal_code":self.postal_code, "password":self.password}

@app.route("/customer")
def get_all():
    return jsonify ({"Customers":[customer.json() for customer in Customer.query.all()]}), 200

@app.route("/customer/<string:telehandle>")
def find_by_Telehandle(telehandle):
    customer_details = Customer.query.filter_by(telehandle = telehandle).first()
    if customer_details:
        return jsonify(customer_details.json()), 201
    return jsonify({"message":"Customer not found"}), 404

@app.route("/login/<string:telehandle>/<string:password>")
def login(telehandle, password):
    customer_details = Customer.query.filter_by(telehandle = telehandle).first()
    if customer_details:
        if customer_details.password == password:
            return jsonify({"message": True, "customer_details": customer_details.json()}), 201
    return jsonify({"message": False}), 404

@app.route("/register/<string:telehandle>", methods=['POST'])
def create_customer(telehandle):
    if (Customer.query.filter_by(telehandle=telehandle).first()):
        return jsonify({"message": "A customer with telehandle '{}' already exists.".format(telehandle)}),400
        
    data = request.get_json()

    customer = Customer(telehandle, **data)
    
    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify({"message":"An error occured creating the customer."}),500

    return jsonify(customer.json()), 201    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug = True)

