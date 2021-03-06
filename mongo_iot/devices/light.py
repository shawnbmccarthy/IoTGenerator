"""
light.py

In our demo we are using dollhouse lights which are connected to relays, as well as a single switch.

"""
from datetime import datetime as dt
from .base_sensor import Sensor

import RPi.GPIO as GPIO

ON=GPIO.LOW
OFF=GPIO.HIGH


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
        GPIO.setup(self._sensor_info['pin'], GPIO.OUT)
        # turn off light
        GPIO.output(self._sensor_info['pin'], OFF)
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
        self._logger.debug('attempting to light sensor data')
        return {
            'device_id': self.device_id,
            'sensor_name': self.sensor_name,
            'sensor_type': self.sensor_type,
            'sensor_id': self.sensor_id,
            'n_samples': self.get_sample_size(),
            'timestamp': dt.now(),
            'value': GPIO.input(self._sensor_info['pin'])
        }

    def execute_cmd(self, cmd):
        """
        TODO: Document relay weirdness!

        :param cmd:
        :return:
        """
        self._logger.info('running light sensor command')
        if cmd:
            self._logger.info('setting light pin to low (turn light on)')
            GPIO.output(self._sensor_info['pin'], ON)
        else:
            self._logger.info('setting light pin to high (turn lights off)')
            GPIO.output(self._sensor_info['pin'], OFF)
        return self.get_sensor_data()

    def register_event(self, evt_logger):
        """

        :param evt_logger:
        :return:
        """
        pass


    def event_callback(self, evt):
        """
        TODO: Implement what? and how?

        :param evt:
        :return:
        """
        pass
