import argparse
from urllib import response
import markdown
import shelve
import os

from flask_restful import Resource, Api, reqparse
from datetime import date, datetime
from flask import Flask, g
from random import randint


def create_app(testing=False, db_name = "my_db.db"):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if testing:
        app.config.update({"TESTING": True,})

    # Create Flask instance
    app = Flask(__name__)

    # Create API!
    api = Api(app)


    def get_db(db_name):

        # g is a flask object for storing data during the application context of a running Flask web app
        
        db = getattr(g, '_database', None)

        if db is None:
            db = g._database = shelve.open(f"./data/{db_name}", writeback=True)
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

    def make_response(query):
        metric, stat, start, end = query['Metric'],query['Statistic'],query['Start Date'],query['End Date']
        #TODO Implement this!
        return str(randint(1,100))

    #########################################################################################

    class Query(Resource):

        def get(self, query_id):

            db = get_db(db_name)
            
            # If the key does not exist in the data store, return a 404 error.
            if (query_id not in db.keys()):
                return {'message': 'Query not found', 'data': {}}, 404

            query = db[query_id]

            db.close()

            return {'message': 'Success', 'data': query}, 200        

    #########################################################################################

    class QueryList(Resource):

        def get(self):
            db = get_db(db_name)
            keys = list(db.keys())

            query_list = []

            for key in keys:
                if (key.startswith('query_')):
                    query_list.append(db[key])

            db.close()

            return {'message': 'Success', 'data': query_list}, 200

    #########################################################################################

    class SensorQuery(Resource):

        def post(self,sensor_id):
            
            parser = reqparse.RequestParser()
            parser.add_argument('Metric', required=True)
            parser.add_argument('Statistic', required=True)
            parser.add_argument('Start Date', required=False)
            parser.add_argument('End Date', required=False)

            # get sensor db
            db = get_db(db_name)

            if sensor_id in db.keys():

                 # create query from arg parser
                args = parser.parse_args()
        
                #make unique(ish) query_id
                query_id = 'query_' + sensor_id + '_' + datetime.now().strftime("%m%d%Y%H%M%S")  
                metric = args['Metric']
                stat = args['Statistic']
                start = args['Start Date']
                end = args['End Date'] 
                response = make_response(args)

                query = {'QueryID':query_id, 'SensorID':sensor_id, 'Metric':metric, 'Statistic':stat, 'Start Date':start, 'End Date':end, 'Response':response}

                # store query in query db on QueryID
                db[query_id] = query

                db.close()

                message = query_id 
                data = query
                code = 201

            else:
                message =  f'Sensor: {sensor_id} not found'
                data = '' 
                code = 403

            return {'message': message, 'data': data}, code

    #########################################################################################

    class SensorList(Resource):

        def get(self):
            db = get_db(db_name)

            keys = list(db.keys())

            sensor_list = []

            for key in keys:
                if(key.startswith('sensor_')):
                    sensor_list.append(db[key])

            db.close()

            return {'message': 'Success', 'data': sensor_list}, 200

        def post(self):
            parser = reqparse.RequestParser()

            parser.add_argument('SensorID', required=True)
            parser.add_argument('Gateway', required=True)

            args = parser.parse_args()

            # Parse the arguments into an object
            sensor_id = 'sensor_' + args['SensorID']
            gateway = args['Gateway']

            sensor = {'SensorID':sensor_id, 'Gateway': gateway}
            
            db = get_db(db_name)

            db[sensor_id] = sensor

            db.close()

            return {'message': 'Sensor registered', 'data': sensor['SensorID']}, 201

    #########################################################################################

    class Sensor(Resource):
        def get(self, sensor_id):
            db = get_db(db_name)

            # If the key does not exist in the data store, return a 404 error.
            if (sensor_id not in db.keys()):
                return {'message': 'Sensor not found', 'data': {}}, 404

            db.close()
            
            return {'message': 'Sensor found', 'data': sensor_id}, 200

        def delete(self, sensor_id):
            db = get_db(db_name)

            # If the key does not exist in the data store, return a 404 error.
            if (sensor_id not in db):
                return {'message': 'Sensor not found', 'data': {}}, 404

            del db[sensor_id]

            db.close()

            return f'Sensor {sensor_id} deregistered', 204
    
    #########################################################################################

    api.add_resource(SensorQuery, '/queries/<sensor_id>') #POST QUERY to a sensor
    api.add_resource(QueryList, '/queries') #GET queries
    api.add_resource(Query, '/query/<query_id>') #GET and DELETE queries
    api.add_resource(SensorList, '/sensors' ) #POST SENSOR
    api.add_resource(Sensor, '/sensor/<sensor_id>') #GET and DELETE sensors

    return app
