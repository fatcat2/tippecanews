from datetime import datetime

from influxdb import InfluxDBClient

def log(message: str):
    print(f"{datetime.now()}: {message}")

def log_request(endpoint: str="/"):
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'tippecanews')
    json_body = [
        {
            "measurement": "requests",
            "tags": {
                "endpoint": endpoint,
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": 1
            }
        }
    ]
    client.write_points(json_body)

def log_error(function: str):
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'tippecanews')
    json_body = [
        {
            "measurement": "errors",
            "tags": {
                "function": function,
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": 1
            }
        }
    ]
    client.write_points(json_body)

if __name__ == "__main__":
    log("Hello")