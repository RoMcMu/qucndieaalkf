

def test_home_page_get(client):

    """
    GIVEN a Flask API
    WHEN the '/' page is sent a GET request
    THEN confirm correct response
    """

    response = client.get('/')

    print(response)
#####Finish this test!!!

    assert response != 404



def test_register_sensor(client):

    """
    GIVEN a Flask API
    WHEN the a sensor is registered via POST at this endpoint: /sensors
    THEN confirm response is 201
    """
    
    body = {'SensorID':'test_id', 'Gateway':'123.123.123'}
    endpoint = '/sensors'
    response = client.post(endpoint, data = body)
    
    assert response.status_code == 201



def test_sensor_get_all(client):

    """
    GIVEN a Flask API
    WHEN more than one sensor is registered and a GET request is sent to this endpoint: '/sensors'
    THEN confirm response is 200
    """

    body_1 = {'SensorID':'test_id_get_all_sensors_1', 'Gateway':'123.123.123'}
    body_2= {'SensorID':'test_id_get_all_sensors_2', 'Gateway':'123.123.123'}
    endpoint = '/sensors'
    client.post(endpoint, data = body_1)
    client.post(endpoint, data = body_2)
    response = client.get(endpoint)
    
    assert response.status_code == 200



def test_sensor_get_individual_success(client):

    """
    GIVEN a Flask API
    WHEN at least one sensor is registered and a get request is sent to '/sensors/<regisered_sensor_id>
    THEN confirm response is 200
    """

    body_1 = {'SensorID':'test_id_get_individual_sensor', 'Gateway':'123.123.123'}
    endpoint = '/sensors'
    client.post(endpoint, data = body_1)
    endpoint = '/sensor/sensor_test_id_get_individual_sensor'
    response = client.get(endpoint)
    
    assert response.status_code == 200



def test_sensor_get_individual_fail(client):

    """
    GIVEN a Flask API
    WHEN get request is sent to '/sensors/<sensor_id> with an invalid <sensor_id>
    THEN confirm response is 404
    """
    endpoint = '/sensor/sensor_test_id_get_individual_sensor_fail'
    response = client.get(endpoint)
    
    assert response.status_code == 404



def test_query_post(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to '/queries/<sensor_id>' with a valid <sensor_id>
    THEN confirm response is 201
    """

    body = {'Metric':'test_metric', 'Statistic':'test_stat', 'Start Date':'11/11/2022', 'End Date':'12/11/2022'}
    endpoint = '/queries/sensor_test_id'
    response = client.post(endpoint, data = body)
    
    assert response.status_code == 201



def test_query_post_non_existing_sensor(client):

    """
    GIVEN a Flask API
    WHEN a correct query is made via a POST request to '/queries/<sensor_id>' with an invalid <sensor_id>
    THEN confirm response is 403
    """

    body = {'Metric':'test_metric', 'Statistic':'test_stat', 'Start Date':'11/11/2022', 'End Date':'12/11/2022'}
    endpoint = '/queries/sensor_missing_sensor'
    response = client.post(endpoint, data = body)
    
    assert response.status_code == 403



def test_query_get_all(client):

    """
    GIVEN a Flask API
    WHEN multiple queries have been successfully posted a GET request is sent to '/queries'
    THEN confirm response is 200
    """

    body_1 = {'Metric':'test_metric_1', 'Statistic':'test_stat_1', 'Start Date':'11/11/2022', 'End Date':'12/11/2022'}
    body_2 = {'Metric':'test_metric_2', 'Statistic':'test_stat_2', 'Start Date':'11/11/2022', 'End Date':'12/11/2022'}
    
    endpoint = '/queries'
    
    client.post(endpoint, data = body_1)
    client.post(endpoint, data = body_2)

    response = client.get(endpoint)

    assert response.status_code == 200



def test_query_get_individual(client):

    """
    GIVEN a Flask API
    WHEN at least one query exists and a GET request is sent to /query/<query_id> with a existing value for <query_id>
    THEN confirm response is 200
    """   

    body = {'Metric':'test_metric', 'Statistic':'test_stat', 'Start Date':'11/11/2022', 'End Date':'12/11/2022'}
    endpoint = '/queries/sensor_test_id'
    response = client.post(endpoint, data = body)
    endpoint = '/query/' + response.json['message']
    response = client.get(endpoint)

    assert response.status_code == 200



def test_sensor_delete(client):

    """
    GIVEN a Flask API
    WHEN a sensor is registered and a DELETE request is sent to /sensor/<sensor_id> with a valid, registered value for <sensor_id>
    THEN confirm response is 204
    """

    sensor_id = 'test_id_to_delete'

    body = {'SensorID':sensor_id, 'Gateway':'123.123.123'}
    endpoint = '/sensors'
    client.post(endpoint, data = body)

    endpoint = '/sensor/sensor_' + sensor_id

    print(endpoint)

    response = client.delete(endpoint)

    assert response.status_code == 204