import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import InfluxDBClient
from kafka import KafkaConsumer
from aws_iot import IoTDataPlane

class IoTData:
    def __init__(self, iot_client: IoTDataPlane, kafka_bootstrap_servers: str, influxdb_host: str, influxdb_port: int):
        self.iot_client = iot_client
        self.kafka_consumer = KafkaConsumer('iot_data', bootstrap_servers=kafka_bootstrap_servers)
        self.influxdb_client = InfluxDBClient(host=influxdb_host, port=influxdb_port)
        self.influxdb_client.switch_database('iot_data')

    def ingest_iot_data(self) -> None:
        for message in self.kafka_consumer:
            data = message.value.decode('utf-8')
            json_data = json.loads(data)
            self.influxdb_client.write_points(self._convert_to_influxdb_points(json_data))

    def _convert_to_influxdb_points(self, json_data: dict) -> List[Dict[str, Any]]:
        points = []
        for device_id, device_data in json_data.items():
            for sensor_id, sensor_data in device_data.items():
                point = {
                    'measurement': 'iot_data',
                    'tags': {
                        'device_id': device_id,
                        'sensor_id': sensor_id
                    },
                    'fields': {
                        'value': sensor_data['value'],
                        'unit': sensor_data['unit']
                    },
                    'time': datetime.utcfromtimestamp(sensor_data['timestamp'])
                }
                points.append(point)
        return points

    def query_iot_data(self, device_id: str, sensor_id: str, start_time: str, end_time: str) -> pd.DataFrame:
        query = f"SELECT * FROM iot_data WHERE device_id = '{device_id}' AND sensor_id = '{sensor_id}' AND time >= '{start_time}' AND time <= '{end_time}'"
        result = self.influxdb_client.query(query)
        return pd.DataFrame(result.get_points())

    def get_device_list(self) -> List[str]:
        query = "SHOW TAG VALUES FROM iot_data WITH KEY = 'device_id'"
        result = self.influxdb_client.query(query)
        return [row['value'] for row in result.get_points()]

    def get_sensor_list(self, device_id: str) -> List[str]:
        query = f"SHOW TAG VALUES FROM iot_data WITH KEY = 'sensor_id' WHERE device_id = '{device_id}'"
        result = self.influxdb_client.query(query)
        return [row['value'] for row in result.get_points()]
