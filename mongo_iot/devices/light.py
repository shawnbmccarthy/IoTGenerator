from datetime import datetime as dt
from .base_sensor import Sensor

import RPi.GPIO as GPIO

class Light(Sensor):
    def __init__(self, device_id, sensor_id, sensor_name, sensor_info, polling_seconds=5, bucket_size=200):
        """

        :param device_id:
        :param sensor_id:
        :param sensor_name:
        :param sensor_info:
        :param polling_seconds:
        :param bucket_size:
        """
        super(Light, self).__init__(
            device_id,
            sensor_id,
            'LIGHT',
            sensor_name,
            sensor_info,
            polling_seconds,
            bucket_size
        )

    def setup_device(self):
        """

        :return:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._sensor_info['pin'], GPIO.OUT)
        self.current_state = GPIO.input(self._sensor_info['pin'])
        return {
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'current_state': self.current_state
        }

    def get_sensor_data(self):
        """

        :return:
        """
        self._logger.debug('attempting to get sensor data')
        return {
            'device_id': self.device_id,
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'n_samples': self.get_sample_size(),
            'timestamp': dt.now(),
            'value': GPIO.input(self._sensor_info['pin'])
        }