import argparse
from urllib import response
import markdown
import shelve
import ast
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


    def get_db(db_name):

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


    @app.route('/query/<query_id>', methods=['GET'])
    def get_query(query_id):

        db = get_db(db_name)
        
        # If the query_id does not exist in the data store, return a 404 error.
        if (query_id not in db.keys()):
            return {'message': 'Query not found', 'data': {}}, 404

        query = db[query_id]

        db.close()

        return {'message': 'Success', 'data': query}, 200  



    @app.route('/query', methods=['POST'])
    def post_query():

            parser = reqparse.RequestParser()
            parser.add_argument("SensorID", required=True, type=str)
            parser.add_argument('Metric', required=True, type=str)
            parser.add_argument('Statistic', required=True, type=str)
            parser.add_argument('Start Date', required=False, type=str)
            parser.add_argument('End Date', required=False, type=str)
        
            db = get_db(db_name)

            args = parser.parse_args()

            sensor_id = args['SensorID']

            response = {}

            success = False

            if sensor_id == 'all':
                keys = db.keys()
                sensor_ids = []

                for k in keys:
                    if k.startswith('sensor_'):
                        sensor_ids.append(k)

                    for sensor_id in sensor_ids:
                        # create query from arg parser
                        args = parser.parse_args()
                
                        #make unique(ish) query_id
                        query_id = 'query_' + sensor_id + '_' + datetime.now().strftime("%m%d%Y%H%M%S")  

                        metric = args['Metric']
                        stat = args['Statistic']
                        start = args['Start Date']
                        end = args['End Date'] 
                        queried_value = make_response(args)

                        query = {'QueryID':query_id, 
                                'SensorID':sensor_id, 
                                'Metric':metric, 
                                'Statistic':stat, 
                                'Start Date':start, 
                                'End Date':end, 
                                'Queried Value': queried_value}

                        # store query in query db on QueryID
                        db[query_id] = query

                        response[query_id] = query
                        message = query_id
                        success = True
                    

            elif sensor_id is not None: # if sensor_ids is not empty (True)
                
                if sensor_id in db.keys():
                    
                    # create query from arg parser
                    args = parser.parse_args()
            
                    #make unique(ish) query_id
                    query_id = 'query_' + sensor_id + '_' + datetime.now().strftime("%m%d%Y%H%M%S")  

                    metric = args['Metric']
                    stat = args['Statistic']
                    start = args['Start Date']
                    end = args['End Date'] 
                    queried_value = make_response(args)

                    query = {'QueryID':query_id, 
                            'SensorID':sensor_id, 
                            'Metric':metric, 
                            'Statistic':stat, 
                            'Start Date':start, 
                            'End Date':end, 
                            'Queried Value': queried_value}

                    # store query in query db on QueryID
                    db[query_id] = query

                    response[query_id] = query
                    message = query_id
                    success = True

                else:
                    message = ''
                    response['ERROR'] = f'Sensor: {sensor_id} not found'
                    code = 403

            if success == True:
                code = 200

            db.close()

            return {'message': message, 'data': response}, code


    @app.route('/queries', methods=['GET'])     
    def get_all_queries():

        db = get_db(db_name)
        keys = list(db.keys())

        query_list = []

        for key in keys:
            if (key.startswith('query_')):
                query_list.append(db[key])

        db.close()

        return {'message': 'Success', 'data': query_list}, 200


    @app.route('/sensors', methods=['GET'])
    def get_all_sensors():

        db = get_db(db_name)

        keys = list(db.keys())

        sensor_list = []

        for key in keys:
            if(key.startswith('sensor_')):
                sensor_list.append(db[key])

        db.close()

        return {'message': 'Success', 'data': sensor_list}, 200


    @app.route('/sensors', methods=['POST'])
    def register_sensor():

        parser = reqparse.RequestParser()

        parser.add_argument('SensorID', required=True)
        parser.add_argument('Latitude', required=True)
        parser.add_argument('Longitude', required=True)
        parser.add_argument('Gateway', required=True)

        args = parser.parse_args()

        # Parse the arguments into an object
        sensor_id = 'sensor_' + args['SensorID']

        sensor = {'SensorID':sensor_id, 
                  'Gateway':args['Gateway'], 
                  'Latitude':args['Latitude'], 
                  'Longitude':args['Longitude'] }
        
        db = get_db(db_name)

        db[sensor_id] = sensor

        db.close()

        return {'message': 'Sensor registered', 'data': sensor['SensorID']}, 201
    

    @app.route('/sensor/<sensor_id>', methods=['GET'])
    def get_sensor(sensor_id):
        db = get_db(db_name)

        # If the key does not exist in the data store, return a 404 error.
        if (sensor_id not in db.keys()):
            return {'message': 'Sensor not found', 'data': {}}, 404

        db.close()
        
        return {'message': 'Sensor found', 'data': sensor_id}, 200


    @app.route('/sensor/<sensor_id>', methods=['DELETE'])
    def deregister_sensor(sensor_id):
        db = get_db(db_name)

        # If the key does not exist in the data store, return a 404 error.
        if (sensor_id not in db):
            return {'message': 'Sensor not found', 'data': {}}, 404

        del db[sensor_id]

        db.close()

        return {'message': f'Sensor {sensor_id} Deregistered'}, 204
    

    return app
