# sensor_data_processor.py

import os
import time
import threading
import queue
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sensor_data_management.database import SensorDatabase
from sensor_data_management.config import Config

class SensorDataProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.database = SensorDatabase(self.config.database_url)
        self.sensor_data_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self.process_sensor_data)
        self.processing_thread.daemon = True
        self.model = None

    def start_processing(self):
        self.processing_thread.start()

    def process_sensor_data(self):
        while True:
            sensor_data = self.sensor_data_queue.get()
            if sensor_data is None:
                break
            self.process_sensor_data_item(sensor_data)
            self.sensor_data_queue.task_done()

    def process_sensor_data_item(self, sensor_data: dict):
        # Preprocess sensor data
        sensor_data = self.preprocess_sensor_data(sensor_data)

        # Store sensor data in database
        self.database.store_sensor_data(sensor_data)

        # Train machine learning model
        if self.model is None or self.config.retrain_model_interval <= 0:
            self.train_machine_learning_model()

        # Make predictions using machine learning model
        predictions = self.make_predictions(sensor_data)

        # Store predictions in database
        self.database.store_predictions(predictions)

    def preprocess_sensor_data(self, sensor_data: dict) -> dict:
        # Convert sensor data to numerical values
        sensor_data['temperature'] = float(sensor_data['temperature'])
        sensor_data['humidity'] = float(sensor_data['humidity'])
        sensor_data['pressure'] = float(sensor_data['pressure'])

        # Normalize sensor data
        sensor_data['temperature'] = (sensor_data['temperature'] - self.config.temperature_mean) / self.config.temperature_std
        sensor_data['humidity'] = (sensor_data['humidity'] - self.config.humidity_mean) / self.config.humidity_std
        sensor_data['pressure'] = (sensor_data['pressure'] - self.config.pressure_mean) / self.config.pressure_std

        return sensor_data

    def train_machine_learning_model(self):
        # Load sensor data from database
        sensor_data = self.database.load_sensor_data()

        # Split sensor data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(sensor_data.drop('label', axis=1), sensor_data['label'], test_size=0.2, random_state=42)

        # Train random forest classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate machine learning model
        y_pred = self.model.predict(X_test)
        print('Model accuracy:', accuracy_score(y_test, y_pred))
        print('Model classification report:')
        print(classification_report(y_test, y_pred))

    def make_predictions(self, sensor_data: dict) -> dict:
        # Make predictions using machine learning model
        predictions = self.model.predict(sensor_data)

        # Convert predictions to dictionary
        predictions_dict = {'prediction': predictions[0], 'probability': predictions[1]}

        return predictions_dict

    def add_sensor_data(self, sensor_data: dict):
        self.sensor_data_queue.put(sensor_data)

    def stop_processing(self):
        self.sensor_data_queue.put(None)
        self.processing_thread.join()

if __name__ == '__main__':
    config = Config()
    processor = SensorDataProcessor(config)
    processor.start_processing()

    # Add sensor data to processing queue
    sensor_data = {'temperature': 25.0, 'humidity': 60.0, 'pressure': 1013.25, 'label': 0}
    processor.add_sensor_data(sensor_data)

    # Stop processing
    processor.stop_processing()
