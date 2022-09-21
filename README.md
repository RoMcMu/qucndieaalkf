# qucndieaalkf

# Weather Sensor API

## Usage

Response from:

```json
{
    "body": "Body of the response",
    "status": "Status information"
}
```
<br>
<br>
### Display list of sensors

**Definition**

`GET /sensors`

**Response**

- `200 OK` on success

```json
[
    {
        "SensorID": "",
        "Lontitude": "",
        "Latitude": "",
        "Gateway": ""
    },
    {
        "SensorID": "",
        "Lontitude": "",
        "Latitude": "",
        "Gateway": ""
    }
]
```
<br>
<br>
### Display Individual Sensor

**Definition**

`GET /sensor/<sensor_id`

**Response**

- `200 OK` on success
- `404 Not Found` if the device does not exist

```json
[
    {
        "SensorID": "",
        "Lontitude": "",
        "Latitude": "",
        "Gateway": ""
    }
]
```

<br>
<br>
### Register a new sensor

**Definition**

`POST /sensors`

**Argument List**

- `"SensorID"`  A unique identifier for the sensor.
- `"Latitude"`  The latitude GPS value of the sensor.
- `"Longitude"` The longitude GPS value of the sensor.
- `"Gateway"`   The IP address of the sensor.

**Response**

- `201 Sensor Registered Successfully` on success

```json
{
    "SensorID": "",
    "Latitude": "",
    "Longitude": "",
    "Gateway": ""
}
```
<br>
<br>
### Deregister a sensor.

**Definition**

`DELETE /sensor/<sensor_id>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` on success

<br>
<br>
### Post a Query to a Single Sensor

`POST /queries/<sensor_id>`

**Response**

- `403 Not Found` if the sensor being posted to does not exist
- `200 OK` on success

```json
{
    "Metric": "",
    "Statistic": "",
    "Start Date": "",
    "End Date": ""
}
```
<br>
<br>
### Display all Queries

**Definition**

`GET /queries`

**Response**

- `200 OK` on success

```json
[
    {
        "QueryID": "",
        "SensorID": "",
        "Metric": "",
        "Statistic": "",
        "Start Date": "",
        "End Date": "",
        "Response": ""
    },

    {
        "QueryID": "",
        "SensorID": "",
        "Metric": "",
        "Statistic": "",
        "Start Date": "",
        "End Date": "",
        "Response": ""
    }
]
```
<br>
<br>
### Display Individual Query

**Definition**

`GET /query/<query_id`

**Response**

- `200 OK` on success
- `404 Not Found` if the device does not exist

```json
[
    {
        "QueryID": "",
        "SensorID": "",
        "Metric": "",
        "Statistic": "",
        "Start Date": "",
        "End Date": "",
        "Response": ""
    }
]
```
