from __future__ import print_function
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import great_circle
import requests

# scheduler
from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
from datetime import date
from os import environ

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika
import json
import uuid

app = Flask(__name__)
app.debug = True
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('routing_db_url', "mysql+mysqlconnector://root@localhost:3306/routing")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Routing(db.Model):
    __tablename__ = 'routing'

    routing_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, primary_key = True)
    telehandle = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable = False)
    postal_code = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False)
    timeslot = db.Column(db.String(2), nullable=True)
    delivery_status = db.Column(db.String(30), nullable=False)

    def __init__(self, routing_id, order_id, telehandle, address, postal_code, date, timeslot, delivery_status):
        self.routing_id = routing_id
        self.order_id = order_id
        self.telehandle = telehandle
        self.address = address
        self.postal_code = postal_code
        self.date = date
        self.timeslot = timeslot
        self.delivery_status = delivery_status

    def json(self):
        return {
            "routing_id" : self.routing_id,
            "order_id" : self.order_id,
            "telehandle" : self.telehandle,
            "address" : self.address,
            "postal_code" : self.postal_code,
            "date" : self.date,
            "timeslot" : self.timeslot,
            "delivery_status" : self.delivery_status
        }

@app.route("/")
def sensor():
    print("Scheduler is alive!")
    return "Scheduler has started"

@app.route("/<string:routing_id>")
@app.route("/tsp/<string:routing_id>")
def tsp(routing_id):
    return render_template("index.html", routing_id = routing_id)

@app.route("/telehandle/<int:order_id>/<int:routing_id>")
def show(order_id, routing_id):
    routing_obj = Routing.query.filter_by(order_id = order_id, routing_id = routing_id).first()

    return routing_obj.json()["telehandle"], 200

@app.route("/tspSolver/<string:routing_id>")
def tspSolver(routing_id):
    locations = [(1.296846462, 103.8522079)]
    address = ["81 VICTORIA STREET SINGAPORE MANAGEMENT UNIVERSITY SINGAPORE 188065"]
    routing_obj = ["start"]
    if Routing.query.filter_by(routing_id = routing_id, delivery_status = 'Pending').all():
        [
            (locations.append(get_coords_backend(routing.json()["postal_code"], "coords")),
            address.append(get_coords_backend(routing.json()["postal_code"], "address")),
            routing_obj.append(routing.json()))
            for routing in Routing.query.filter_by(routing_id = routing_id, delivery_status = 'Pending').all()
        ]

    num_vehicles = 1
    data = create_data_model(locations, address, num_vehicles, routing_obj)
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])
    data['distance_matrix'] = [list(distance_matrix[key].values()) for key in distance_matrix]

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
    search_parameters.time_limit.seconds = 30

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        solution_data = solution_dict(data, manager, routing, solution)

    return solution_data

@app.route("/geojsonFeature/<string:coords>")
def geojsonFeature(coords):

    route_coords = eval(coords)

    body = {"coordinates":route_coords}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': '5b3ce3597851110001cf62484ec3813bdd294730a43dad978a1025dc',
        'Content-Type': 'application/json; charset=utf-8'
    }

    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-hgv/geojson', json=body, headers=headers)

    return call.text, call.status_code

def get_coords_backend(pcode, task):
    mapsURL = f'http://developers.onemap.sg/commonapi/search?searchVal={pcode}&returnGeom=Y&getAddrDetails=Y&pageNum=1'
    
    while True:
        try:
            response = requests.get(mapsURL).json()
        except requests.exceptions.ConnectionError as e:
            time.sleep(2)
            continue

        if response['totalNumPages'] > 0:
            results = response['results'][0]
            break
        else:
            return {"message": "invalid address"}
            break
    
    if task == "coords":
        return (float(results['LATITUDE']), float(results["LONGITUDE"]))
    
    elif task == 'address':
        return results['ADDRESS']

def solution_dict(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    tsp_sol = {}
    for vehicle_id in range(data['num_vehicles']):
        tsp_sol[vehicle_id] = {"plan_output": [], "address_txt": [], "dist": 0, "routing_obj": []}
        index = routing.Start(vehicle_id)

        route_distance = 0
        while not routing.IsEnd(index):
            tsp_sol[vehicle_id]['plan_output'].append(manager.IndexToNode(index))
            tsp_sol[vehicle_id]['address_txt'].append(data['address'][manager.IndexToNode(index)])
            tsp_sol[vehicle_id]['routing_obj'].append(data['routing_obj'][manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        if route_distance > 0:
            tsp_sol[vehicle_id]['dist'] = route_distance
            tsp_sol[vehicle_id]['plan_output'].append(manager.IndexToNode(index))
            tsp_sol[vehicle_id]['address_txt'].append(data['address'][manager.IndexToNode(index)])
            tsp_sol[vehicle_id]['routing_obj'].append(data['routing_obj'][manager.IndexToNode(index)])
            max_route_distance = max(route_distance, max_route_distance)
        else:
            tsp_sol[vehicle_id]['dist'] = route_distance
            tsp_sol[vehicle_id]['plan_output'] = []
            tsp_sol[vehicle_id]['address_txt'] = []
            tsp_sol[vehicle_id]['routing_obj'] = []


    return {"tsp": tsp_sol, "max_dist": max_route_distance, "data" : data}

def create_data_model(locations, address, num_vehicles, routing_obj):
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data['locations'] = locations # yapf: disable
    data['address'] = address
    data['num_vehicles'] = num_vehicles
    data['routing_obj'] = routing_obj
    data['depot'] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = great_circle(from_node, to_node).km
    return distances

@app.route("/send_orders/<int:routing_id>")
def send_order(routing_id):
    data = tspSolver(routing_id)['tsp']

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
    message = json.dumps(data, default=str) # convert a JSON object to a string

    # Prepare the correlation id and reply_to queue and do some record keeping
    corrid = str(uuid.uuid4())
    # prepare the channel and send a message to Shipping
    channelqueue = channel.queue_declare(queue='routing.order', durable=True) # make sure the queue used by Shipping exist and durable
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='routing.order') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="routing.order", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
            correlation_id=corrid # set the correlation id for easier matching of replies
        )
    )

    # close the connection to the broker
    connection.close()
    return "good", 200

def receiveRouteUpdate():

    rabbit_host = environ.get('rabbit_host', 'localhost') # default host
    port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=port))
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="route_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct', durable=True)

    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue='routing.update', durable=True) # '' indicates a random unique queue name; 'exclusive' indicates the queue is used only by this receiver and will be deleted if the receiver disconnects.
        # If no need durability of the messages, no need durable queues, and can use such temp random queues.
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='routing.update') # bind the queue to the exchange via the key
        # Can bind the same queue to the same exchange via different keys

    # set up a consumer and start to wait for coming messages, stop upon 5 seconds of inactivity
    results = []
    for method, properties, body in channel.consume(queue=queue_name, inactivity_timeout=5):
        if body == None:
            print("no more message")
            break

        results.append(json.loads(body))

        # Acknowledge the message
        channel.basic_ack(method.delivery_tag)

    connection.close()
    print(results)
    if len(results) > 0:
        for result in results:
            output = update_delivery_status(result['order_id'], result['routing_id'], result['delivery_status'])
            print(output)

def get_customer_details(telehandle):
    customerURL = environ.get('customer_url', "http://localhost:5000/customer/") + telehandle
    print(customerURL)
    try:
        r = requests.get(customerURL, timeout=1)
    except requests.exceptions.RequestException as e:
        return jsonify({"message": e}), 503


    result = eval(r.text)
    address_details = {"address" : result["address"], "postal_code": result["postal_code"]}

    return address_details

@app.route('/testing_chat/<string:telehandle>')
def get_chat_id(telehandle):
    telegram_poll_url = environ.get('telegram_poll_url', "http://localhost:8990/") + f"getChatId/{telehandle}"
    # print(telegram_poll_url)
    try:
        r = requests.get(telegram_poll_url, timeout=1)
    except requests.exceptions.RequestException as e:
        return jsonify({"message": e}), 503

    # print(r.text)
    try:
        return r.text
    except:
        return ""
    
def update_telegram_users(chat_ids, delivery_status = "Your order is on delivery"):
    telegram_url = environ.get('telegram_url', "http://127.0.0.1:8989/")
    # print(telegram_url)
    for chat_id in chat_ids:
        order_str = f"{delivery_status}\n" + "\n".join(chat_ids[chat_id]) + "\nThank you for purchasing with us"
        send_url = f"{telegram_url}message/{chat_id}"

        send_message = {'message': order_str}
        try:
            r = requests.post(send_url, json=send_message)

        except:
            print("error")

def update_delivery_status(order_id, routing_id, delivery_status):

    routing_obj = Routing.query.filter_by(order_id = order_id, routing_id = routing_id).first()

    
    if delivery_status != routing_obj.delivery_status:
        routing_obj.delivery_status = delivery_status
        try:
            db.session.commit()
        except:
            return "Error in updating record"

    return routing_obj.json()
    
@app.route("/route_details/<int:order_id>")
def get_route_obj(order_id):
    routing_obj = Routing.query.filter_by(order_id = order_id).first()

    if routing_obj:
        return jsonify(routing_obj.json())
    else:
        return "error"

@app.route("/processRoute", methods = ["POST"])
def processRoute():
    data = json.loads(request.get_json())
    batch_data_purchase = data['delivery']

    last_route = Routing.query.order_by(Routing.routing_id.desc()).first()
    if last_route == None:
        new_route_id = 1
    else:
        new_route_id = last_route.routing_id + 1
    routing_details = []
    chat_ids = {}
    for data_purchase in batch_data_purchase:
        '''
        data_purchase = {
            "order_id" : <int>,
            "telehandle" : "@BoredBryan",
            "date" : <date>,
            "timeslot" : <str>
            "product" : <str>
            "quantity" : <int>
        }

        data_customer = {
            "address" : <str>,
            "postal_code" : <int>
        }
        '''
        order_id = data_purchase['order_id']

        if Routing.query.filter_by(order_id = order_id).first():
            pass
        else:
            data_customer = get_customer_details(data_purchase['telehandle'])

            chat_id = get_chat_id(data_purchase["telehandle"])
            print(chat_id)
            if chat_id != '':
                if int(chat_id) not in chat_ids:
                    chat_ids[int(chat_id)] = []
                product = data_purchase['product']
                quantity = data_purchase["quantity"]
                chat_ids[int(chat_id)].append(f"Order no. {new_route_id}-{data_purchase['order_id']}: {product} x {quantity}")
            


            data_stored = {
                "order_id": data_purchase['order_id'],
                "telehandle": data_purchase['telehandle'],
                "date": data_purchase['date'],
                'timeslot' : data_purchase['timeslot']
            }

            RoutingObj = Routing(routing_id=new_route_id,delivery_status="Pending", **data_stored, **data_customer)
            routing_details.append(RoutingObj.json())
            try:
                db.session.add(RoutingObj)
                db.session.commit()
            except:
                return jsonify({"message":"An error occured creating the furniture."}), 500

    # send_order(new_route_id)
    telegram_url = environ.get('telegram_url', "http://127.0.0.1:8989/") + 'receiveUrl/' + str(new_route_id)
    r = requests.get(telegram_url)
    # print(chat_ids)
    update_telegram_users(chat_ids)


    return jsonify({"message": "Successfully sent URL!"}), 201

@app.before_first_request
def before_first_request():
    if not app.debug or environ.get("WERKZEUG_RUN_MAIN") == "true":
        sched = BackgroundScheduler()
        sched.add_job(receiveRouteUpdate, 'interval', seconds=10)
        sched.start()


if __name__ == "__main__":


    app.run(port=5006, host='0.0.0.0')
