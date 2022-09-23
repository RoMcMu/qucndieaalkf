import json

test_lat = "37.701475274672525"
test_long = "-122.46976818886122"
test_gateway = "0.0.0.0"

def test_home_page_get(client):

    """
    GIVEN a Flask API
    WHEN the "/" page is sent a GET request
    THEN confirm correct response
    """

    response = client.get("/")

    print(response)
    
    assert response.status_code == 200



def test_register_sensor(client):

    """
    GIVEN a Flask API
    WHEN the a sensor is registered via POST at this endpoint: /sensors
    THEN confirm response is 201
    """
    # register test sensor
    body = {"SensorID":"test_id", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"

    response = client.post(endpoint, json = body)
    
    assert response.status_code == 201



def test_sensor_get_all(client):

    """
    GIVEN a Flask API
    WHEN more than one sensor is registered and a GET request is sent to this endpoint: "/sensors"
    THEN confirm response is 200
    """

    endpoint = "/sensors"

    # register test sensor 1
    body_1 = {"SensorID":"test_id_get_all_sensors_1", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    client.post(endpoint, json = body_1)

    # register test sensor 1
    body_2= {"SensorID":"test_id_get_all_sensors_2", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    client.post(endpoint, json = body_2)    

    response = client.get(endpoint)
    
    assert response.status_code == 200



def test_sensor_get_individual_success(client):

    """
    GIVEN a Flask API
    WHEN at least one sensor is registered and a get request is sent to "/sensors/<regisered_sensor_id>
    THEN confirm response is 200
    """
    endpoint = "/sensors"

    # register test sensor
    body = {"SensorID":"test_id_get_individual_sensor", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    client.post(endpoint, json = body)

    endpoint = "/sensor/sensor_test_id_get_individual_sensor"
    response = client.get(endpoint)
    
    assert response.status_code == 200



def test_sensor_get_individual_fail(client):

    """
    GIVEN a Flask API
    WHEN get request is sent to "/sensors/<sensor_id> with an invalid <sensor_id>
    THEN confirm response is 404
    """
    endpoint = "/sensor/sensor_test_id_get_individual_sensor_fail"
    response = client.get(endpoint)
    
    assert response.status_code == 404


def test_query_post_single_sensor(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to "/query"
    THEN confirm response is 201
    """

    # register test sensor
    body = {"SensorID":"test_id_individual", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    # POST query to test sensor
    body = {"SensorIDs" : ["sensor_test_id_individual"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    endpoint = "/query"
    response = client.post(endpoint, json = body)

    assert response.status_code == 200



def test_query_post_multi_sensor(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to "/query" containing multiple sensor ids
    THEN confirm response is 201
    """

    # register test sensor 1
    body = {"SensorID":"test_id_multi_1", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    # register test sensor 2
    body = {"SensorID":"test_id_multi_2", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    # register test sensor 3
    body = {"SensorID":"test_id_multi_3", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    # POST query to test sensor
    body = {"SensorIDs" : ["sensor_test_id_multi_1", "sensor_test_id_multi_2", "sensor_test_id_multi_3"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    endpoint = "/query"
    print(json.dumps(body))
    response = client.post(endpoint, json = body)

    assert response.status_code == 200



def test_query_post_all_sensors(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to "/query" with keyword 'all'
    THEN confirm response is 201
    """

    # POST query to test sensor
    body = {"SensorIDs" : ["all"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    endpoint = "/query"
    response = client.post(endpoint, json = body)

    assert response.status_code == 200



def test_query_post_non_existing_sensor(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to "/query" with an invalid <sensor_id>
    THEN confirm response is 403
    """

    body = {"SensorIDs" : ["test_id_individual_sensor_non_existant"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    endpoint = "/query"
    response = client.post(endpoint, json = body)
    
    assert response.status_code == 403



def test_query_get_all(client):

    """
    GIVEN a Flask API
    WHEN multiple queries have been successfully posted a GET request is sent to "/queries"
    THEN confirm response is 200
    """
    endpoint = "/queries"

    # register test sensor 1
    body_1 = {"SensorIDs" : ["test_id_individual_sensor_1"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    client.post(endpoint, json = body_1)
    
    # register test sensor 1
    body_2 = {"SensorIDs" : ["test_id_individual_sensor_2"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    client.post(endpoint, data = body_2)
 
    response = client.get(endpoint)

    assert response.status_code == 200



def test_query_get_individual(client):

    """
    GIVEN a Flask API
    WHEN at least one query exists and a GET request is sent to /query/<query_id> with a existing value for <query_id>
    THEN confirm response is 200
    """   

    # register test sensor
    body = {"SensorID":"test_id_individual", "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    # POST test query
    body = {"SensorIDs" : ["sensor_test_id_individual"], "Metric":"test_metric", "Statistic":"test_stat", "Start Date":"11/11/2022", "End Date":"12/11/2022"}
    endpoint = "/query"
    response = client.post(endpoint, json = body)
    print(response)
    endpoint = '/query/' + response.json['message']

    response = client.get(endpoint)
    assert response.status_code == 200



def test_query_get_individual_invalid_query_id(client):

    """
    GIVEN a Flask API
    WHEN at least one query exists and a GET request is sent to /query/<query_id> with a non-existing value for <query_id>
    THEN confirm response is 200
    """   
    bad_query_id = "bad_query_id_value"
    endpoint = "/query/" + bad_query_id
    response = client.get(endpoint)

    assert response.status_code == 404



def test_sensor_delete(client):

    """
    GIVEN a Flask API
    WHEN a sensor is registered and a DELETE request is sent to /sensor/<sensor_id> with a valid, registered value for <sensor_id>
    THEN confirm response is 204
    """

    sensor_id = "test_id_to_delete"

    body = {"SensorID":sensor_id, "Gateway":test_gateway, "Latitude": test_lat, "Longitude": test_long}
    endpoint = "/sensors"
    client.post(endpoint, json = body)

    endpoint = "/sensor/sensor_" + sensor_id

    response = client.delete(endpoint)

    assert response.status_code == 204



def test_sensor_delete_bad_sensor_id(client):

    """
    GIVEN a Flask API
    WHEN a sensor is registered and a DELETE request is sent to /sensor/<sensor_id> with a valid, registered value for <sensor_id>
    THEN confirm response is 204
    """

    sensor_id = "bad_sensor_id"

    endpoint = "/sensor/sensor_" + sensor_id

    response = client.delete(endpoint)

    assert response.status_code == 404