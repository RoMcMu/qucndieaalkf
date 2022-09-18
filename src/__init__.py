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

def get_db():

    # g is a flask object for storing data during the application context of a running Flask web app
    
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = shelve.open("mock.db")

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

def make_response(query):
    metric, stat, start, end = query['Metric'],query['Statistic'],query['Start Date'],query['End Date']
    #TODO Implement this!
    return str(randint(1,100))

#########################################################################################

class Query(Resource):

    def get(self, query_id):

        shelf = get_db()
        
        # If the key does not exist in the data store, return a 404 error.
        if (query_id not in shelf):
            return {'message': 'Query not found', 'data': {}}, 404

        return {'message': 'Success', 'data': shelf[query_id]}, 200        

#########################################################################################

class QueryList(Resource):

    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        queries = []

        for key in keys:
            queries.append(shelf[key])

        return {'message': 'Success', 'data': queries}, 200

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('SensorID', required=True)
        parser.add_argument('Metric', required=True)
        parser.add_argument('Start Date', required=False)
        parser.add_argument('End Date', required=False)

        # get db
        shelf = get_db()
        # create query from arg parser
        query = parser.parse_args()
        # store query in db on QueryID
        shelf[query["QueryID"]] = query

        # I am making the below respone to imitate the actual
        # response retuned from the imaginary sensor being queried.
        # make_response() will return an appropriate value based on the metric passed.
        response = make_response(query)

        return {'message': 'Query successful', 'data': response}, 201

    def delete(self, query_id):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if (query_id not in shelf):
            return {'message': 'Query not found', 'data': {}}, 404

        del shelf[query_id]

        return f'Query: {query_id} deleted', 204

#########################################################################################

class DBCheck(Resource):

    def get(self):

        shelf = get_db()
        query_keys = list(shelf.keys())

        queries = []

        for key in query_keys:
            queries.append(shelf[key])

        return queries

#########################################################################################

api.add_resource(QueryList, '/queries/<sensor_id>')
api.add_resource(Query, '/query/<query_id>')
