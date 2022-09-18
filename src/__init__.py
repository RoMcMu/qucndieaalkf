import argparse
import markdown
import shelve
import os

from flask_restful import Resource, Api, reqparse
from datetime import date, datetime
from flask import Flask, g
from random import randint

# Create Flask instance
app = Flask(__name__)

# Create API!
api = Api(app)

def get_sensor_db():

    # g is a flask object for storing data during the application context of a running Flask web app
    
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = shelve.open("sensor.db")

    return db

def get_query_db():

    # g is a flask object for storing data during the application context of a running Flask web app
    
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = shelve.open("query.db")

    return db

@app.teardown_appcontext
def teardown_db(exception):

    db = getattr(g, '_database', None)

    if db is not None:
        db.close()

@app.route("/")
def readme():
    
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        content = markdown_file.read()

        return markdown.markdown(content)

def cli_interface():
    # Create the parser
    arg_parser = argparse.ArgumentParser(description='Enter a query: -sensor -metric -stat -start (dd/mm/yyyy) -end (dd/mm/yyyy)')

    # Add the arguments
    arg_parser.add_argument('SensorID',
                       metavar='sensor_id',
                       type=str,
                       help='ID of requested sensor')
    
    arg_parser.add_argument('Metric',
                       metavar='metric',
                       type=str,
                       help='Metric to be queried')

    arg_parser.add_argument('Statistc',
                       metavar='stat',
                       type=str,
                       help='Statistic to be applied to metric')

    arg_parser.add_argument('StartDate',
                       metavar='start date',
                       type=date,
                       help='Start date of query, dd/mm/yyyy')    

    arg_parser.add_argument('EndDate',
                       metavar='end date',
                       type=date,
                       help='End date of query, dd/mm/yyyy')

    args = arg_parser.parse_args()

    return args

def make_response(query):
    metric, stat, start, end = query['Metric'],query['Statistic'],query['Start Date'],query['End Date']
    #TODO Implement this!
    return str(randint(1,100))

#########################################################################################

class Query(Resource):

    def get(self, query_id):

        shelf = get_query_db()
        
        # If the key does not exist in the data store, return a 404 error.
        if (query_id not in shelf):
            return {'message': 'Query not found', 'data': {}}, 404

        return {'message': 'Success', 'data': shelf[query_id]}, 200        

#########################################################################################

class QueryList(Resource):

    def get(self):
        shelf = get_query_db()
        keys = list(shelf.keys())

        queries = []

        for key in keys:
            queries.append(shelf[key])

        return {'message': 'Success', 'data': queries}, 200

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('SensorID', required=True)
        parser.add_argument('Metric', required=True)
        parser.add_argument('Statistic', required=True)
        parser.add_argument('Start Date', required=False)
        parser.add_argument('End Date', required=False)

        # get db
        shelf = get_query_db()
        # create query from arg parser
        query = parser.parse_args()
        #make unique(ish) query_id
        query_id = query['SensorID'] + datetime.now().strftime("%m%d%Y%H%M%S")
        
        query['QueryID'] = (query_id)
        # store query in db on QueryID
        shelf[query["QueryID"]] = query

        # I am making the below respone to imitate the actual
        # response retuned from the imaginary sensor being queried.
        # make_response() will return an appropriate value based on the metric passed.
        response = make_response(query)

        return {'message': 'Query successful', 'data': response}, 201

    def delete(self, query_id):
        shelf = get_query_db()

        # If the key does not exist in the data store, return a 404 error.
        if (query_id not in shelf):
            return {'message': 'Query not found', 'data': {}}, 404

        del shelf[query_id]

        return f'Query: {query_id} deleted', 204

#########################################################################################

class SensorList(Resource):

    def get(self):
        shelf = get_sensor_db()
        keys = list(shelf.keys())

        sensors = []

        for key in keys:
            sensors.append(shelf[key])

        return {'message': 'Success', 'data': sensors}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('SensorID', required=True)
        parser.add_argument('Gateway', required=True)
        parser.add_argument('Queries', required=False)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_sensor_db()
        shelf[args["SensorID"]] = args

        return {'message': 'Sensor registered', 'data': args}, 201

#########################################################################################

class Sensor(Resource):
    def get(self, sensor_id):
        shelf = get_sensor_db()

        # If the key does not exist in the data store, return a 404 error.
        if (sensor_id not in shelf):
            return {'message': 'Sensor not found', 'data': {}}, 404

        return {'message': 'Sensor found', 'data': shelf[sensor_id]}, 200

    def delete(self, sensor_id):
        shelf = get_query_db()

        # If the key does not exist in the data store, return a 404 error.
        if (sensor_id not in shelf):
            return {'message': 'Sensor not found', 'data': {}}, 404

        del shelf[sensor_id]
        return '', 204

#########################################################################################

class DBCheck(Resource):

    def get(self):

        shelf = get_query_db()
        query_keys = list(shelf.keys())

        queries = []

        for key in query_keys:
            queries.append(shelf[key])

        return queries

#########################################################################################

api.add_resource(QueryList, '/sensor/queries')
api.add_resource(Query, '/sensor/query/<query_id>')
api.add_resource(SensorList, '/sensors' )
api.add_resource(Sensor, '/sensor/<sensor_id>')
