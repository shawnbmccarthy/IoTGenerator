from datetime import datetime as dt
from .base_sensor import Sensor
import RPi.GPIO as GPIO

DOOR_OPEN = 1
DOOR_CLOSED = 0

class Door(Sensor):
    def __init__(self, device_id, sensor_id, sensor_name, sensor_info, polling_seconds=5, bucket_size=200):
        """

        :param device_id:
        :param sensor_id:
        :param sensor_loc_name:
        :param sensor_info:
        :param polling_s: amount of polling to do every cycle
        """
        super(Door, self).__init__(device_id, sensor_id, 'DOOR', sensor_name, sensor_info, polling_seconds, bucket_size)

    def setup_device(self):
        """

        :return:
        """
        GPIO.setup(self._sensor_info['pin'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
        self._logger.debug('attempting to get door sensor data')
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

        :param cmd:
        :return:
        """
        self._logger.info('running door command (DO NOTHING)')
        pass

    def register_event(self, evt_logger):
        """

        :param evt_logger:
        :return:
        """
        self._logger.info('setting up door event handler (pin:{})'.format(self._sensor_info['pin']))
        self._evt_logger = evt_logger
        GPIO.add_event_detect(self._sensor_info['pin'], GPIO.BOTH, callback=self.event_callback)

    def event_callback(self, evt):
        """
        TODO: Implement rise and fall -> need to test

        :param evt:
        :return:
        """
        self._logger.info('executing door event')
        evt_data = self.get_sensor_data()
        if GPIO.input(self._sensor_info['pin']): # 1
            evt_data['msg'] = 'door is open'
            evt_data['evt_type'] = 'DOOR_OPEN'
        else:
            evt_data['msg'] = 'door is closed'
            evt_data['evt_type'] = 'DOOR_CLOSED'

        self._logger.info('emitting door event: {}'.format(evt_data))
        self._evt_logger.emit_event(evt_data)