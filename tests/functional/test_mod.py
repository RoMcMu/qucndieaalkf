def test_home_page_get(client):
    """
    GIVEN a Flask API
    WHEN the '/' page is sent a GET request
    THEN confirm correct response
    """

    response = client.get('/')
    assert response != 404

def test_sensor_get():
    pass