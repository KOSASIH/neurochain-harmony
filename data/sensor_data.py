import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from sklearn.preprocessing import StandardScaler

class SensorData:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def clean_data(self) -> pd.DataFrame:
        self.data.dropna(inplace=True)
        self.data.interpolate(method='linear', inplace=True)
        return self.data

    def filter_data(self, window_size: int, poly_order: int) -> pd.DataFrame:
        self.data['value'] = savgol_filter(self.data['value'], window_size, poly_order)
        return self.data

    def scale_data(self) -> pd.DataFrame:
        scaler = StandardScaler()
        self.data['value'] = scaler.fit_transform(self.data['value'].values.reshape(-1, 1))
        return self.data

    def detect_anomalies(self, threshold: float) -> pd.DataFrame:
        self.data['anomaly'] = np.where(self.data['value'] > threshold, 1, 0)
        return self.data

    def visualize_data(self) -> None:
        import matplotlib.pyplot as plt
        plt.plot(self.data['time'], self.data['value'])
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Sensor Data')
        plt.show()
