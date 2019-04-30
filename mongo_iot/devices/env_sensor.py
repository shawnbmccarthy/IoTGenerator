from datetime import datetime as dt
from .base_sensor import Sensor

import adafruit_bme280
import board
import busio

class EnvSensor(Sensor):
    def __init__(self, device_id, sensor_id, sensor_name, sensor_info, polling_seconds=5, bucket_size=200):
        super(EnvSensor, self).__init__(
            device_id,
            sensor_id,
            'ENV_SENSOR',
            sensor_name,
            sensor_info,
            polling_seconds,
            bucket_size
        )

    def setup_device(self):
        """

        :return:
        """
        self._bme280 = adafruit_bme280.Adafruit_BME280_I2C(busio.I2C(board.SCL, board.SDA))
        self._bme280.sea_level_pressure = self._sensor_info['sea_level_pressure']
        self.current_state = getattr(self._bme280, self._sensor_info['measurement'])
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
        self._logger.debug('attempting to get environment sensor data')
        return {
            'device_id': self.device_id,
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'n_samples': self.get_sample_size(),
            'timestamp': dt.now(),
            'value': getattr(self._bme280, self._sensor_info['measurement'])
        }

    def execute_cmd(self, cmd):
        """

        :param cmd:
        :return:
        """
        self._logger.info('running environment sensor command')
        return self.get_sensor_data()

    def register_event(self, evt):
        """
        TODO: Implement breaches maybe?

        :param evt:
        :return:
        """
        pass