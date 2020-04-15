from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('furniture_db_url', "mysql+mysqlconnector://root@localhost:3306/product")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Furniture(db.Model):
    __tablename__ = 'product'

    product_name = db.Column(db.String(64), nullable = False)
    product_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable = False)
    price = db.Column(db.Float(precision=2), nullable = False)
    image = db.Column(db.String(200), nullable = False)
    quantity= db.Column(db.Integer)
    

    def __init__(self, product_id, product_name, category, price, image, quantity):
        self.product_name = product_name
        self.product_id = product_id
        self.category = category
        self.price = price
        self.image = image
        self.quantity = quantity

    def json(self):
        return {"product_name": self.product_name, "product_id":self.product_id, "image":self.image, "category":self.category,
        "price":self.price, "quantity":self.quantity}

@app.route("/furniture")
def get_all():
    return jsonify ({"Furnitures":[furniture.json() for furniture in Furniture.query.all()]}), 201

@app.route("/furniture/<string:product_name_input>")
def find_by_productid(product_name_input):
    furniture = Furniture.query.filter(Furniture.product_name.contains(product_name_input)).all()
    try:
        if furniture:
            return jsonify({"Furnitures":[furnitures.json() for furnitures in furniture]}), 201
        return jsonify({"message":"Furniture not found."}),201
    except:
        return jsonify({"message":"error occur while querying database"}), 404

@app.route("/furniture/<string:product_id>", methods=['POST'])
def create_product(product_id):
    if (Furniture.query.filter_by(product_id=product_id).first()):
        return jsonify({"message": "A furniture with productID '{}' already exists".format(product_id)}),400
        
    data = request.get_json()

    furniture = Furniture(product_id, **data)

    try:
        db.session.add(furniture)
        db.session.commit()
    except:
        return jsonify({"message":"An error occured creating the furniture."}),500

    return jsonify(furniture.json()), 201

@app.route("/decrease/<string:product_id_input>/<string:decrement>", methods=['POST'])
def decrease_product(product_id_input, decrement):
    try:
        decrement = int(decrement)
    except Exception as e:
        return jsonify({"message":"Error " + str(e)}), 400
    furniture = Furniture.query.filter(Furniture.product_id.contains(product_id_input)).first()
    # print(type(furniture))
    furniture.quantity = furniture.quantity - decrement
    try:
        db.session.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"message":"Error" + str(e)}), 500

    # result = db.engine.execute("<SET quantity = quantity - " + decrement + "1 where product_id=" + product_id_input + ";>")

@app.route("/furniture/product/<string:product_id>")
def find_productid(product_id):
    product_array = product_id.split(',')
    # furniture = Furniture.query(Furniture).filter(Furniture.product_id.in_(product_array)).from_self()
    furniture = Furniture.query.filter(Furniture.product_id.in_(product_array)).all()
    try:
        if furniture:
            return jsonify({"Furniture":[furnitures.json() for furnitures in furniture]}), 201
        return jsonify({"message":"Furniture not found."}),201
    except:
        return jsonify({"message":"error occur while querying database"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug = True)